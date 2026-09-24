#!/bin/bash
set -euo pipefail

# Build script for .deb package used to install on linux platforms
if ! command -v fakeroot >/dev/null 2>&1; then
    echo "Error: fakeroot is required to build the .deb package. Install it with: sudo apt-get install fakeroot" >&2
    exit 1
fi

if ! command -v dpkg-deb >/dev/null 2>&1; then
    echo "Error: dpkg-deb is required to build the .deb package. Install the dpkg package on Debian/Ubuntu." >&2
    exit 1
fi

# Version to be used as the 'release version'
VERSION="1.0.5"

# Update version in control file
sed -i -e "s/^Version: .*/Version: $VERSION/" ./DEBIAN/control

# Make temp dir
TMP_DIR=$(mktemp -d)

# Copy deb package descriptors and scripts in the DEBIAN folder
cp -R "./DEBIAN" "$TMP_DIR"

RESOURCE_FOLDER_PATH="../python_package/ezdmb/resources"
mkdir -p "$RESOURCE_FOLDER_PATH"

BUILD_RESOURCE_PATH="../python_package/build/lib/ezdmb/resources"
mkdir -p "$BUILD_RESOURCE_PATH"

# Build .deb
OUTPUT_DEB_FILE="$RESOURCE_FOLDER_PATH/ezdmb_${VERSION}_all.deb"
rm -f $RESOURCE_FOLDER_PATH/*.deb
fakeroot dpkg-deb --build "$TMP_DIR" $OUTPUT_DEB_FILE

# Copy deb to python package build resources folder
rm -f $BUILD_RESOURCE_PATH/*.deb
cp "$OUTPUT_DEB_FILE" "$BUILD_RESOURCE_PATH/ezdmb_${VERSION}_all.deb"

# Copy deb to python package build resources folder
rm -f $BUILD_RESOURCE_PATH/*.deb
cp "$OUTPUT_DEB_FILE" "$BUILD_RESOURCE_PATH/ezdmb_${VERSION}_all.deb"

echo "Deb package build complete: $OUTPUT_DEB_FILE"
