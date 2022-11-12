#!/bin/bash

sudo apt install python3-pip pyqt5-dev-tools aqtinstall
sudo pip install -U 
sudo pip install -r requirements.txt
sudo aqt install-qt linux desktop 5.15.2
export PATH="/home/$SUDO_USER/ezdmb/5.15.2/gcc_64/bin":$PATH

