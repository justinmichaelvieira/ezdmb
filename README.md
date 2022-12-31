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

1. Run the environment install script in a bash terminal: `chmod +x ./setup-dev-environment.sh && ./setup-dev-environment.sh`
2. Run the app: `python3 -m ezdmb`

## Instructions / Basic Operation
On load, both the fullscreen and configuration windows are loaded.  The configuration window can be simply closed by the user if it is not needed, leaving the fullscreen "menu board display" window open. 

The display in the main screen of the configuration (under the text "Current menu") mirrors the full screen display.

## System configuration
The system can be configured using:
- The "Display Settings" button and related screens
- Manually editing the dmb_config.json file

### Advanced install instructions / troubleshooting install

If the developer install script/procedure does not work for you, try installing manually as follows:

1. Install python libraries: `pip install -r requirements.txt`
2. Install pyqt dev tools: `sudo apt install pyqt5-dev-tools`
3. Install the qt framework loader: `pip install -U pip && pip install aqtinstall`
4. Use the qt framework loader to install v5.15.2: `aqt install-qt linux desktop 5.9.0`
5. Add qt build tools to your path (replace `<username>` in the command with the username on the system): `export PATH="/home/<username>/ezdmb/5.15.2/gcc_64/bin":$PATH`

Note 1: There is a set of .ui files in the View/ folder. If these are updated (usually they are updated with Qt Designer), you would run `python3 setup.py build_ui` to regenerate them.
Note 2: Qt Designer can be installed, on Ubuntu systems, with:
```
sudo apt-get install qttools5-dev-tools
sudo apt-get install qttools5-dev
```

On Windows and Mac, use the Qt Framework install packages provided at https://www.qt.io/

## Code Listing / Technical Documentation

### __main__.py
The main entry point of the code.  Note:  In a lot of scenarios, you will want to run `python3 -m ezdmb` (or the compiled output equivalent) on startup of the OS.

### Configuration.py
Handles configuration of the system, and outputting the config json.

<<<<<<< HEAD
### dmb_config.pro
Qt Designer project file which loads all designer (`*.ui`) files. If you create a new .ui file, be sure to add it to this project.

### Resource files
Resource file is at `ezdmb/Resources/resources.qrc`. In standard `PyQt5` style, the generated `resources.py` class file can be regenerated with:
`pyrcc5 ezdmb/Resources/resources.qrc -o resources.py`.

=======
>>>>>>> 79a553a5a4928394e6f169fc0b92955950b9f190
## Coming Soon
- Installers + binaries for Windows, WinRT, Linux/android, iOS, MacOS
- Option for whether the app loads on OS startup, expanded file types
- Multi monitor support
- Import menu data from json, yaml file
- Menu item and sub item rendering
