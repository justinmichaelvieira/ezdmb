#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"

if ! command -v apt-get >/dev/null 2>&1; then
    echo "Error: this setup script requires Debian- or Ubuntu-based Linux." >&2
    exit 1
fi

run_as_root() {
    if [[ "$(id -u)" -eq 0 ]]; then
        "$@"
    elif command -v sudo >/dev/null 2>&1; then
        sudo "$@"
    else
        echo "Error: sudo is required to install system prerequisites." >&2
        exit 1
    fi
}

has_python_313_or_later() {
    "$1" -c 'import sys; raise SystemExit(sys.version_info < (3, 13))' >/dev/null 2>&1
}

if [[ -r /etc/os-release ]]; then
    . /etc/os-release
fi

PYTHON_BIN=""
if command -v python3.13 >/dev/null 2>&1 && has_python_313_or_later python3.13; then
    PYTHON_BIN="python3.13"
elif command -v python3 >/dev/null 2>&1 && has_python_313_or_later python3; then
    PYTHON_BIN="python3"
elif [[ "${ID:-}" == "ubuntu" ]]; then
    run_as_root apt-get update
    run_as_root apt-get install --yes software-properties-common
    run_as_root add-apt-repository --yes ppa:deadsnakes/ppa
    run_as_root apt-get update
    run_as_root apt-get install --yes python3.13 python3.13-venv
    PYTHON_BIN="python3.13"
else
    echo "Error: Python 3.13 or later is required. Install it before running this script." >&2
    exit 1
fi

if ! has_python_313_or_later "$PYTHON_BIN"; then
    echo "Error: $PYTHON_BIN did not provide Python 3.13 or later." >&2
    exit 1
fi

if [[ "$PYTHON_BIN" == "python3.13" ]]; then
    VENV_PACKAGE="python3.13-venv"
else
    VENV_PACKAGE="python3-venv"
fi

run_as_root apt-get update
run_as_root apt-get install --yes \
    "$VENV_PACKAGE" \
    libdbus-1-3 \
    libegl1 \
    libgl1 \
    libglib2.0-0 \
    libpulse0 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xinput0 \
    libxkbcommon-x11-0

VENV_DIR="$PROJECT_ROOT/.venv"
"$PYTHON_BIN" -m venv "$VENV_DIR"
"$VENV_DIR/bin/python" -m pip install --upgrade pip
"$VENV_DIR/bin/python" -m pip install "$PROJECT_ROOT"

echo "Development environment ready."
echo "Activate it with: source \"$VENV_DIR/bin/activate\""
echo "Run the current source with: PYTHONPATH=src \"$VENV_DIR/bin/python\" -m ezdmb"
