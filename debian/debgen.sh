#!/bin/bash
# Build script for .deb package used to install on linux platforms

# Version to be used as the 'release version'
VERSION="1.0.2"

# Make temp dir
TMP_DIR=$(mktemp -d)

# Copy overlay to temp dir
cp -r "./overlay/"* "$TMP_DIR"

# Copy deb package descriptors and scripts in the DEBIAN folder
cp -r "./DEBIAN" "$TMP_DIR"

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

echo "Deb package build complete."
