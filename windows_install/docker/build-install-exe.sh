#!/bin/bash

# Uses the amake/innosetup  (https://github.com/amake/innosetup-docker) docker image
# to generate a bundled install exe, on any platform that can run docker (linux, win, mac).

# If, for some reason, this script fails, docker/ezdmb-installer.iss can still be used to generate
# a windows installer, with the innosetup IDE, from within Windows.

mkdir artifacts/ &> /dev/null
docker pull amake/innosetup
docker run --name innosetup -v "$PWD:/artifacts" --rm -i amake/innosetup ezdmb-installer.iss &&
echo "Windows installer build complete. Python resources copied; You may now run 'python setup.py bdist_wheel' in the python_package folder."
