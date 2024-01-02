#!/bin/bash
# Install script for debian targets.

# install dependencies
pip install -U pip
pip install aqtinstall

# install qt
aqt install-qt linux desktop 5.15.12

# Run debian package installer for the app
sudo dpkg -i ezdmb_0.9.0_all.deb
