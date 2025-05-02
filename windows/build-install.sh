#!/bin/bash

# Uses the amake/innosetup  (https://github.com/amake/innosetup-docker) docker image
# to generate a bundled install exe, on any platform that can run docker (linux, win, mac).

# If, for some reason, this script fails, docker/ezdmb-installer.iss can still be used to generate
# a windows installer, with the innosetup IDE, from within Windows.

cd windows_install/docker || exit

mkdir artifacts/ &> /dev/null
DOCKER_BUILDKIT=1 sudo docker build -t ezdmb/inno-builder .
docker run --name inno-build-instance -v "$PWD:/work" -v "${PWD}/artifacts:/artifacts" --rm -i ezdmb/inno-builder ezdmb-installer.iss &&
echo "Windows installer build complete. You may now run 'python setup.py bdist_wheel' in the python_package folder."

cd - || exit
