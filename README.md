# ezdmb
A dead-simple digital menu board display and configuration, written in Python.  Engineered to be the simplest, cheapest, fastest way to get your menu to display on **any** tablet or computer.  Ridiculously user friendly, with basic configuration interface.

## How to run through python3 (dev mode)
Setup for executing the python source:

1. Run the environment install script in a bash terminal: `chmod +x ./setup-dev-environment.sh && ./setup-dev-environment.sh`
2. Run the app: `python3 -m ezdmb`

## Instructions / Basic Operation
On load, both the fullscreen and configuration windows are loaded.  The configuration window can be simply closed by the user if it is not needed, leaving the fullscreen "menu board display" window open. 

The display in the main screen of the configuration (under the text "Current menu") mirrors the full screen display. The full screen display can be closed by holding the CTRL key and pressing the ESC key on a hardware keyboard (or on-screen keyboard emulator).

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

### `dmb_config.pro`
Qt Designer project file which loads all designer (`*.ui`) files. If you create a new .ui file, be sure to add it to this project.

### `ezdmb/`
The ezdmb package. Contains source python for the application.

#### `ezdmb/__main__.py`
The main entry point of the application. Note:  In a lot of scenarios, you will want to run `python -m ezdmb` (or the compiled output equivalent) on startup of the OS.

#### `ezdmb/Controller/Configuration.py`
Handles configuration of the system, and outputting the config json.

### `windows_install/`
`build-install-exe.sh` builds the Windows platform installer. This script requires docker installed on the local system - Docker Desktop (https://www.docker.com/products/docker-desktop/) should work on linux and windows platforms.

### `debian/`
Files for building the Debian (linux) platform installer.

## Roadmap
- Load on startup option in win + linux installers
- Multi monitor options
- Import and render menu data from json, yml file
