#!/bin/bash

cd ../../ || exit

# build the exe
pyinstaller --onefile --name ezdmb --distpath src/ezdmb/dist src/ezdmb/__main__.py

cd - || exit

# copy the executable and stylesheet to the overlay folder
mkdir -p src/debian/overlay/opt/ezdmb
cp ../../src/ezdmb/dist/__main__ ../../src/debian/overlay/opt/ezdmb/ezdmb
cp ../../artifacts/style.css ../../src/debian/overlay/opt/ezdmb/style.css
