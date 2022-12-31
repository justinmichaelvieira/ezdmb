#!/bin/bash

pathadd() {
    if [ -d "$1" ] && [[ ":$PATH:" != *":$1:"* ]]; then
        PATH="${PATH:+"$PATH:"}$1"
    fi
}

sudo apt-get update
sudo apt-get -y install git software-properties-common python3-pip pyqt5-dev-tools
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.9
git clone https://github.com/justinmichaelvieira/ezdmb
pip3 install -r requirements.txt
sudo aqt install-qt linux desktop 5.15.2
pathadd "/home/${SUDO_USER}/ezdmb/5.15.2/gcc_64/bin"
