#!/bin/bash
# Install script for debian targets. Can be used by developers to install the app on their own machines.

# install dependencies
pip install -U pip
pip install aqtinstall

# install qt
aqt install-qt linux desktop 5.15.12

# Run debian package installer for the app
sudo dpkg -i ezdmb_0.9.29_all.deb
