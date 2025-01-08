#!/bin/bash

# Uses the amake/innosetup  (https://github.com/amake/innosetup-docker) docker image
# to generate a bundled install exe, on any platform that can run docker (linux, win, mac).

# If, for some reason, this script fails, docker/ezdmb-installer.iss can still be used to generate
# a windows installer, with the innosetup IDE, from within Windows.

cd docker
docker pull amake/innosetup:latest
mkdir -p artifacts
sudo docker run --name innosetup -v "$PWD:/work" -v "${PWD}/artifacts:/artifacts" --rm -i amake/innosetup ezdmb-installer.iss && cp "./ezdmb_x64.exe" "artifacts/ezdmb_x64.exe" &&
cp -f artifacts/ezdmb_x64.exe ${PWD}/../../python_package/ezdmb/resources/ezdmb_x64.exe && echo "Windows installer build complete. Python resources copied; You may now run 'python setup.py bdist_wheel' in the python_package folder."

cd ..
