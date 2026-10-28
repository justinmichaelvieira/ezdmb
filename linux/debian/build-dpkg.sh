#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"

if ! command -v fakeroot >/dev/null 2>&1; then
    echo "Error: fakeroot is required to build the .deb package. Install it with: sudo apt-get install fakeroot" >&2
    exit 1
fi

if ! command -v dpkg-deb >/dev/null 2>&1; then
    echo "Error: dpkg-deb is required to build the .deb package. Install the dpkg package on Debian/Ubuntu." >&2
    exit 1
fi

if [[ ! -d "$PROJECT_ROOT/src/ezdmb" ]]; then
    echo "Error: application source directory not found: $PROJECT_ROOT/src/ezdmb" >&2
    exit 1
fi

VERSION="$(sed -n 's/^Version: //p' "$SCRIPT_DIR/DEBIAN/control")"
if [[ -z "$VERSION" ]]; then
    echo "Error: package Version is missing from $SCRIPT_DIR/DEBIAN/control" >&2
    exit 1
fi

TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT
PACKAGE_ROOT="$TEMP_DIR/package"

mkdir -p \
    "$PACKAGE_ROOT/DEBIAN" \
    "$PACKAGE_ROOT/usr/bin" \
    "$PACKAGE_ROOT/usr/lib/python3/dist-packages" \
    "$PACKAGE_ROOT/usr/share/applications" \
    "$PACKAGE_ROOT/usr/share/icons/hicolor/192x192/apps"

cp "$SCRIPT_DIR/DEBIAN/control" "$PACKAGE_ROOT/DEBIAN/control"
cp -R "$PROJECT_ROOT/src/ezdmb" "$PACKAGE_ROOT/usr/lib/python3/dist-packages/"
find "$PACKAGE_ROOT/usr/lib/python3/dist-packages/ezdmb" -type f \
    \( -name '*_test.py' -o -name '*.spec' \) -delete
find "$PACKAGE_ROOT/usr/lib/python3/dist-packages/ezdmb" -type d -exec chmod 755 {} +
find "$PACKAGE_ROOT/usr/lib/python3/dist-packages/ezdmb" -type f -exec chmod 644 {} +

cat > "$PACKAGE_ROOT/usr/bin/ezdmb" <<'EOF'
#!/bin/sh
exec /usr/bin/python3 -m ezdmb "$@"
EOF
chmod 755 "$PACKAGE_ROOT/usr/bin/ezdmb"

cat > "$PACKAGE_ROOT/usr/share/applications/ezdmb.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=EZDMB
Comment=Digital Menu Board
Exec=/usr/bin/ezdmb
Icon=ezdmb
Terminal=false
Categories=Utility;
EOF

install -m 644 "$PROJECT_ROOT/src/ezdmb/View/images/logo_192x192.png" \
    "$PACKAGE_ROOT/usr/share/icons/hicolor/192x192/apps/ezdmb.png"

OUTPUT_RESOURCE_DIR="$PROJECT_ROOT/linux/python_package/ezdmb/resources"
OUTPUT_BUILD_DIR="$PROJECT_ROOT/linux/python_package/build/lib/ezdmb/resources"
OUTPUT_DEB_FILE="$OUTPUT_RESOURCE_DIR/ezdmb_${VERSION}_all.deb"
mkdir -p "$OUTPUT_RESOURCE_DIR" "$OUTPUT_BUILD_DIR"

fakeroot dpkg-deb --build "$PACKAGE_ROOT" "$OUTPUT_DEB_FILE"
cp "$OUTPUT_DEB_FILE" "$OUTPUT_BUILD_DIR/ezdmb_${VERSION}_all.deb"

echo "Deb package build complete: $OUTPUT_DEB_FILE"
