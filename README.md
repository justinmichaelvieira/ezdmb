# ezdmb

![ezdmb logo](https://github.com/justinmichaelvieira/ezdmb/raw/master/readme_images/logo_crop.png "ezdmb logo")

A dead-simple digital menu board display and configuration, written in Python.  Engineered to be the simplest, cheapest, fastest way to get your menu to display on **any** tablet or computer. Engineered for user-friendliness, with a simple, basic, configuration interface that easily allows rotation of images and quick configuration.

![ezdmb UI](https://github.com/justinmichaelvieira/ezdmb/raw/master/readme_images/sample1.png "ezdmb UI")

## How to run through python3 (dev mode)
1. Run the environment install script in a bash terminal: `chmod +x ./setup-dev-environment.sh && ./setup-dev-environment.sh`
2. Run the app: `python3 -m ezdmb`

## Basic Operation
- On app start, both the Main (fullscreen) and Preview/Configuration windows are shown on the desktop.
- The Settings window can be closed with the "X" icon at top right of the window if further settings changes are not currently needed.
- The 'Esc' key is used to exit the application.
- Clicking or tapping the Main window and then pressing the 'o' key will reopen the Preview/Configuration window.

## Configuration
 "Edit Display Settings" in the "File" dropdown menu of the Settings window allows access to a settings window, which is used to:
 - Add and remove content to display
 - Rotation settings, to allow content to be changed in the Menu Board Display
![Display settings](https://github.com/justinmichaelvieira/ezdmb/raw/master/readme_images/sample2.png "Display settings")

![Settings window up close](https://github.com/justinmichaelvieira/ezdmb/raw/master/readme_images/sample3.png "Configuration window up close")

### Advanced install instructions / troubleshooting install

If the developer install script/procedure does not work for you, try installing manually as follows:

1. Install python libraries: `pip install -r requirements.txt`
2. Install pyqt dev tools: `sudo apt install pyqt5-dev-tools`
3. Install the qt framework loader: `pip install -U pip && pip install aqtinstall`
4. Use the qt framework loader to install v5.15.2: `aqt install-qt linux desktop 5.9.0`
5. Add qt build tools to your path (replace `<username>` in the command with the username on the system): `export PATH="/home/<username>/ezdmb/5.15.2/gcc_64/bin":$PATH`

On Windows and Mac, use the Qt Framework install packages provided at https://www.qt.io/

## Roadmap
- Load on startup option in win + linux installers
- Import and render menu data from json, yml file
