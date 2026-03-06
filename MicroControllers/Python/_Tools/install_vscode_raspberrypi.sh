#!/usr/bin/env bash
set -euo pipefail

# Install Visual Studio Code on Raspberry Pi OS.
# Tries Microsoft build (code) first, then falls back to code-oss.

if [[ "${EUID}" -ne 0 ]]; then
  SUDO="sudo"
else
  SUDO=""
fi

echo "[1/4] Updating package index..."
${SUDO} apt update

echo "[2/4] Checking CPU architecture..."
ARCH="$(dpkg --print-architecture)"
echo "Detected architecture: ${ARCH}"
if [[ "${ARCH}" != "arm64" && "${ARCH}" != "armhf" ]]; then
  echo "Warning: This script is intended for Raspberry Pi architectures (arm64/armhf)."
fi

echo "[3/4] Installing VS Code package..."
if ${SUDO} apt install -y code; then
  INSTALLED_PACKAGE="code"
else
  echo "Package 'code' not available. Trying 'code-oss'..."
  ${SUDO} apt install -y code-oss
  INSTALLED_PACKAGE="code-oss"
fi

echo "[4/4] Verifying installation..."
if command -v code >/dev/null 2>&1; then
  code --version
elif command -v code-oss >/dev/null 2>&1; then
  code-oss --version
else
  echo "Install finished but executable was not found in PATH."
fi

echo
echo "Done. Installed package: ${INSTALLED_PACKAGE}"
