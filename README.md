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

## How to run through python3 (dev mode)
Setup for executing the python source:

1. Install Python3 from (https://www.python.org/downloads/)
2. Clone or download all files in this repo: `git clone https://github.com/justinmichaelvieira/ezdmb`).
3. Install python libraries: `pip install -r requirements.txt`
4. Install pyqt dev tools: `sudo apt install pyqt5-dev-tools`
5. Install the qt framework loader: `pip install -U pip && pip install aqtinstall`
6. Use the qt framework loader to install v5.15.2: `aqt install-qt linux desktop 5.15.2`
7. Add qt build tools to your path: `export PATH="/home/<username>/ezdmb/5.15.2/gcc_64/bin":$PATH`
8. Finally, run the app: `python main.py`

Note: There is a set of .ui files in the View/ folder; If these are updated with Qt Designer, you would run `python3 setup.py build_ui` to regenerate them.

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

## Coming Soon
- Installers + binaries for Windows, WinRT, Linux/android, iOS, MacOS
- Option for whether the app loads on OS startup, expanded file types
- Multi monitor support
- Import menu data from json, yaml file
- Menu item and sub item rendering