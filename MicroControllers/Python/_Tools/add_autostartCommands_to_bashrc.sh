#!/usr/bin/env bash
set -euo pipefail

BASHRC_FILE="${HOME}/.bashrc"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
STARTME_FILE="${PROJECT_DIR}/SoundBox/startme.py"
LINE_STARTME="${PROJECT_DIR}/SoundBox/startme.py &"
LINE_VENV="source ${PROJECT_DIR}/.venv/bin/activate &"

if [[ -f "${STARTME_FILE}" ]]; then
  chmod +x "${STARTME_FILE}"
  echo "Made executable: ${STARTME_FILE}"
else
  echo "Warning: start script not found: ${STARTME_FILE}"
fi

if [[ ! -f "${BASHRC_FILE}" ]]; then
  touch "${BASHRC_FILE}"
fi

for LINE in "${LINE_STARTME}" "${LINE_VENV}"; do
  if grep -Fxq "${LINE}" "${BASHRC_FILE}"; then
    echo "Line already exists in ${BASHRC_FILE}: ${LINE}"
  else
    printf "\n%s\n" "${LINE}" >> "${BASHRC_FILE}"
    echo "Added line to ${BASHRC_FILE}: ${LINE}"
  fi
done
