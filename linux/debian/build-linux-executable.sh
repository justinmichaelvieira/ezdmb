#!/bin/bash

cd ../ezdmb || exit

# build the exe
pyinstaller --onefile --name ezdmb --distpath ../ezdmb/dist ../ezdmb/__main__.py

cd - || exit

# copy the executable and stylesheet to the overlay folder
mkdir -p overlay/opt/ezdmb
cp ../ezdmb/dist/ezdmb overlay/opt/ezdmb/ezdmb
cp ../style.css overlay/opt/ezdmb/style.css
