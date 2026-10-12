#!/usr/bin/env bash
set -euo pipefail

read -r -p "New Version: " NEW_VERSION

if [[ ! "$NEW_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Warning: version must be in x.x.x form (for example, 1.2.3)." >&2
    exit 1
fi

REPO_ROOT="${EZDMB_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
cd "$REPO_ROOT"

case "$(uname -s)" in
    Darwin*)
        SED_IN_PLACE=(-i '')
        SED_FLAGS=(-E)
        ;;
    MINGW*|MSYS*|CYGWIN*)
        SED_IN_PLACE=(-i -b)
        SED_FLAGS=(-E)
        ;;
    *)
        SED_IN_PLACE=(-i)
        SED_FLAGS=(-E)
        ;;
esac

replace_in_file() {
    local expression="$1"
    local file="$2"
    sed "${SED_IN_PLACE[@]}" "${SED_FLAGS[@]}" "$expression" "$file"
}

replace_in_file "s/.*/$NEW_VERSION/" artifacts/.version
replace_in_file "s/(ezdmb_)[0-9]+\\.[0-9]+\\.[0-9]+(_all\\.deb)/\\1${NEW_VERSION}\\2/" debian/install.sh
replace_in_file "s/^(AppVerName=ezdmb v)[0-9]+\\.[0-9]+\\.[0-9]+/\\1${NEW_VERSION}/" ezdmb-installer.iss
replace_in_file "s/^(VERSION=.)[0-9]+\\.[0-9]+\\.[0-9]+/\\1${NEW_VERSION}/" linux/debian/build-dpkg.sh
replace_in_file "s/^(Version: )[0-9]+\\.[0-9]+\\.[0-9]+/\\1${NEW_VERSION}/" linux/debian/DEBIAN/control
replace_in_file "s/^(version = .)[0-9]+\\.[0-9]+\\.[0-9]+/\\1${NEW_VERSION}/" pyproject.toml
replace_in_file "s/^(.*appWheelFile = .ezdmb-)[0-9]+\\.[0-9]+\\.[0-9]+(-py3-none-any\\.whl)/\\1${NEW_VERSION}\\2/" setup-dev-environment.ps1
replace_in_file "s/^(    version=.)[0-9]+\\.[0-9]+\\.[0-9]+/\\1${NEW_VERSION}/" setup.py
replace_in_file "s/^(__version__ = .)[0-9]+\\.[0-9]+\\.[0-9]+/\\1${NEW_VERSION}/" src/ezdmb/__init__.py
sed "${SED_IN_PLACE[@]}" "${SED_FLAGS[@]}" "/^name = .*ezdmb/,/^[[:space:]]*$/ s/^(version = .)[0-9]+\\.[0-9]+\\.[0-9]+/\\1${NEW_VERSION}/" uv.lock

echo "Updated ezdmb version to $NEW_VERSION."
