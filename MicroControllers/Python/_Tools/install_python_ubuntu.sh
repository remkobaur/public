#!/usr/bin/env bash
set -euo pipefail

# Install Python tooling on Ubuntu:
# - python3
# - pip3
# - venv support

if [[ "${EUID}" -ne 0 ]]; then
  SUDO="sudo"
else
  SUDO=""
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REQUIREMENTS_FILE="${PROJECT_DIR}/requirements.txt"
VENV_DIR="${PROJECT_DIR}/.venv"
ALSAAUDIO_FALLBACK_REQUIRED=0
SPIDEV_FALLBACK_REQUIRED=0

echo "[1/6] Updating apt package index..."
${SUDO} apt update

echo "[2/6] Installing python3, python3-pip, python3-venv..."
${SUDO} apt install -y python3 python3-pip python3-venv

echo "[3/6] Verifying installation..."
python3 --version
pip3 --version

if [[ -f "${REQUIREMENTS_FILE}" ]]; then
  APT_HINT_LINE="$(grep -E '^#\s*(sudo\s+)?apt\s+install\s' "${REQUIREMENTS_FILE}" | head -n 1 || true)"
  # Normalize possible CRLF line endings from edited files.
  APT_HINT_LINE="$(printf '%s' "${APT_HINT_LINE}" | tr -d '\r')"
  if [[ -n "${APT_HINT_LINE}" ]]; then
    APT_PACKAGES="$(echo "${APT_HINT_LINE}" | sed -E 's/^#\s*//; s/^(sudo\s+)?apt\s+install\s+(-y\s+)?//')"
    APT_PACKAGES="$(printf '%s' "${APT_PACKAGES}" | tr -d '\r' | xargs)"
    if [[ -n "${APT_PACKAGES}" ]]; then
      echo "[4/6] Installing OS packages from commented requirements hint..."
      # Intentional word splitting: apt expects package names as separate args.
      # shellcheck disable=SC2086
      if ! ${SUDO} apt install -y ${APT_PACKAGES}; then
        if [[ " ${APT_PACKAGES} " =~ (^|[[:space:]])python3-alsaaudio([[:space:]]|$) ]] || [[ " ${APT_PACKAGES} " =~ (^|[[:space:]])python3-spidev([[:space:]]|$) ]]; then
          echo "One or more optional OS packages were not found. Retrying apt install without unsupported packages..."
          APT_PACKAGES_NO_ALSA=""
          for pkg in ${APT_PACKAGES}; do
            if [[ "${pkg}" != "python3-alsaaudio" && "${pkg}" != "python3-spidev" ]]; then
              APT_PACKAGES_NO_ALSA+="${pkg} "
            fi
          done
          APT_PACKAGES_NO_ALSA="$(printf '%s' "${APT_PACKAGES_NO_ALSA}" | xargs || true)"
          if [[ -n "${APT_PACKAGES_NO_ALSA}" ]]; then
            # shellcheck disable=SC2086
            ${SUDO} apt install -y ${APT_PACKAGES_NO_ALSA}
          fi
          if [[ " ${APT_PACKAGES} " =~ (^|[[:space:]])python3-alsaaudio([[:space:]]|$) ]]; then
            ALSAAUDIO_FALLBACK_REQUIRED=1
          fi
          if [[ " ${APT_PACKAGES} " =~ (^|[[:space:]])python3-spidev([[:space:]]|$) ]]; then
            SPIDEV_FALLBACK_REQUIRED=1
          fi
        else
          echo "Failed to install OS packages from requirements hint."
          exit 1
        fi
      fi
    fi
  fi

  echo "[5/6] Creating virtual environment and installing Python packages from ${REQUIREMENTS_FILE}..."
  # Keep apt-installed Python modules (e.g. smbus/cwiid) visible inside the venv.
  python3 -m venv --system-site-packages "${VENV_DIR}"
  "${VENV_DIR}/bin/python" -m pip install --upgrade pip
  "${VENV_DIR}/bin/pip" install -r "${REQUIREMENTS_FILE}"

  if [[ "${ALSAAUDIO_FALLBACK_REQUIRED}" -eq 1 ]]; then
    echo "Installing build dependencies and pyalsaaudio via pip fallback..."
    ${SUDO} apt install -y libasound2-dev python3-dev build-essential swig
    "${VENV_DIR}/bin/pip" install pyalsaaudio
  fi

  if [[ "${SPIDEV_FALLBACK_REQUIRED}" -eq 1 ]]; then
    echo "Installing spidev via pip fallback..."
    "${VENV_DIR}/bin/pip" install spidev
  fi
else
  echo "[4/6] No requirements file found at ${REQUIREMENTS_FILE}; skipping OS and pip package install."
  python3 -m venv --system-site-packages "${VENV_DIR}"
  "${VENV_DIR}/bin/python" -m pip install --upgrade pip
fi

echo "[6/6] Validating runtime dependencies..."
"${VENV_DIR}/bin/python" - <<'PY'
import importlib

required = ["mutagen", "RPi.GPIO", "smbus", "spidev", "alsaaudio"]
missing = []
for module_name in required:
    try:
        importlib.import_module(module_name)
        print(f"OK: {module_name}")
    except Exception as exc:
        print(f"MISSING: {module_name} ({exc})")
        missing.append(module_name)

if missing:
    raise SystemExit(f"Missing Python modules: {', '.join(missing)}")
PY

if command -v mpg123 >/dev/null 2>&1; then
  echo "OK: mpg123 available"
else
  echo "MISSING: mpg123 (install with: sudo apt install -y mpg123)"
  exit 1
fi

echo
echo "Done. To activate the created virtual environment:"
echo "  source ${VENV_DIR}/bin/activate"
echo "  python -m pip install --upgrade pip"
echo "  python -c 'import smbus; print(\"smbus OK\")'"
echo "  python -c 'import spidev; print(\"spidev OK\")'"
