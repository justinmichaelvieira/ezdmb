# ezdmb
A dead-simple digital menu board display and configuration, written in Python.  Engineered to be the simplest, cheapest, fastest way to get your menu to display on **any** tablet or computer.  Ridiculously user friendly, with basic configuration interface.
### Full screen screenshot
![Full Screen Menu Image](/Images/354580462_orig.jpg)
### Configuration window (1)
![Configuration Window 1](/Images/ezdmb1.PNG)
### Configuration window (2)
![Configuration Window 2](/Images/ezdmb2.PNG)
### Configuration window (3)
![Configuration Window 3](/Images/ezdmb3.PNG)

## Prerequisites
- Python 3 (https://www.python.org/downloads/)
- Qt 5 (https://www.qt.io/)

## How to run
1. Clone or download all files (be sure to include and install the prerequisites above, if you don't have them)!
2. Run `pip install -r requirements.txt` in the directory.
3. Open a command line, and run `main.py` in the local ezdmb folder.  For example, on Windows I might run `python main.py`.

## Instructions / Basic Operation
On load, both the fullscreen and configuration windows are loaded.  The configuration window can be simply closed by the user if it is not needed, leaving the fullscreen "menu board display" window open. 

The display in the main screen of the configuration (under the text "Current menu") mirrors the full screen display.

## System configuration
The system can be configured using:
- The "Display Settings" button and related screens
- Manually editing the dmb_config.json file
   

## Code Listing / Technical Documentation

### main.py
The main entry point of the code.  Note:  In a lot of scenarios, you will want to run `python main.py` (or the compiled output equivalent) on startup of the OS.

### Configuration.py
Handles configuration of the system, and outputting the config json.

### dmb_config.pro
Qt Designer project file which loads all designer (`*.ui`) files.

### `*_auto.py`
The `*_auto.py` are generated from Qt designer files using the `pyuic5` command (see: http://manpages.ubuntu.com/manpages/xenial/man1/pyuic5.1.html). 

## Coming Soon
- Installers + binaries for Windows, WinRT, Linux/android, iOS, MacOS
- Option for whether the app loads on OS startup, expanded file types
- Multi monitor support
- Import menu data from json, yaml file
- Menu item and sub item rendering