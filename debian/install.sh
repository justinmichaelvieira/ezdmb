#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
CONTROL_FILE="$PROJECT_ROOT/linux/debian/DEBIAN/control"

if ! command -v apt-get >/dev/null 2>&1; then
    echo "Error: apt-get is required to install the Debian package and its dependencies." >&2
    exit 1
fi

VERSION="$(sed -n 's/^Version: //p' "$CONTROL_FILE")"
if [[ -z "$VERSION" ]]; then
    echo "Error: package Version is missing from $CONTROL_FILE" >&2
    exit 1
fi

DEB_FILE="$PROJECT_ROOT/linux/python_package/ezdmb/resources/ezdmb_${VERSION}_all.deb"
if [[ ! -f "$DEB_FILE" ]]; then
    echo "Error: package not found: $DEB_FILE" >&2
    echo "Build it first with: bash linux/debian/build-dpkg.sh" >&2
    exit 1
fi

run_as_root() {
    if [[ "$(id -u)" -eq 0 ]]; then
        "$@"
    elif command -v sudo >/dev/null 2>&1; then
        sudo "$@"
    else
        echo "Error: sudo is required to install the package." >&2
        exit 1
    fi
}

run_as_root apt-get update
run_as_root apt-get install --yes "$DEB_FILE"
