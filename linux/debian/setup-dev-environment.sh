#!/bin/bash

pathadd() {
    if [ -d "$1" ] && [[ ":$PATH:" != *":$1:"* ]]; then
        PATH="${PATH:+"$PATH:"}$1"
    fi
}

sudo apt-get update
sudo apt-get -y install git software-properties-common python3-pip python3-pyside6.qttools fakeroot
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.9
git clone https://github.com/justinmichaelvieira/ezdmb
pip3 install -r ../requirements.txt
sudo aqt install-qt linux desktop 6.9.0
pathadd "/home/${SUDO_USER}/ezdmb/6.9.0/gcc_64/bin"
