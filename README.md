# ezdmb
A dead-simple digital menu board display and configuration, written in Python.  Engineered to be the simplest, cheapest, fastest way to get your menu to display on **any** tablet or computer.  Ridiculously user friendly, with one button configuration interface.
### Full screen screenshot
![Full Screen Menu Image](/Images/354580462_orig.jpg)
### Configuration window
![Configuration Window](/Images/ezdmb1.PNG)

## Prerequisites
Python 3 (https://www.python.org/downloads/)
Qt 5 (https://www.qt.io/)

## How to run
1. Clone or download all files (be sure to include and install the prerequisites above, if you don't have them)!
2. Open a command line, and run `main.py` in the local ezdmb folder.  For example, on Windows I might run `python c:\Users\Justin\Documents\ezdmb\main.py`.

## Instructions / Basic Operation
The "Set New Image" button opens a file browser on the tablet/computer which will allow the user to select a different image.  On selection a config file, `dmb_config.json`, is written with the name of the selected menu board image.

## Code Listing / Technical Documentation

### main.py
The main entry point of the code.  Note:  In a lot of scenarios, you will want to run `python main.py` (or the compiled output equivalent) on startup of the OS.

### Configuration.py
Handles configuration of the system, and outputting the config json.

### /Controller/SelectFile.py
File selection dialog behavior and overrides.

### /dmb_config.pro
Qt project file which loads all designer (`*.ui`) files.

### `*_auto.py`
The `*_auto.py` are generated from Qt designer files using the `pyuic5` command (see: http://manpages.ubuntu.com/manpages/xenial/man1/pyuic5.1.html). 

## Coming Soon
- Bug fixes (ongoing)
- Installers for Windows, WinRT, Linux/android, iOS, MacOS
  - Will include option for whether the app loads on OS startup
- "Premium" edition with backend API and multiple menu rendering options (import price list, HTML, etc)