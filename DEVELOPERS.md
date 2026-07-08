# How to run through python3 (local dev env setup)

## Ubuntu Linux

1. Run the install script in a bash terminal: `chmod +x ./setup-dev-environment.sh && ./setup-dev-environment.sh`
2. Run the app: `python3 -m ezdmb`

## Windows

1. Install Python if necessary: <https://www.python.org/downloads/windows/>
2. Clone the ezdmb repo using `git clone https://github.com/justinmichaelvieira/ezdmb.git`, or the big green "<> Code" button on <https://github.com/justinmichaelvieira/ezdmb>
3. Run `setup-dev-environment.ps1` in the root folder of the repo.

`py __main__.py` should allow you to run that app. Debug messages will be logged every time the display content updates. The content update interval can be changed using `File > Settings` .

## Advanced install instructions / troubleshooting install

If the developer install script/procedure does not work for you, try installing manually as follows:

1. Install python libraries: `pip install -r requirements.txt`
2. Install PySide6 dev tools: `sudo apt install python3-pyside6.qttools`
3. Install the qt framework loader: `pip install -U pip && pip install aqtinstall`
4. Use the qt framework loader to install Qt 6 if needed; otherwise PySide6 is installed via pip.
5. Add qt build tools to your path (replace `<username>` in the command with the username on the system): `export PATH="/home/<username>/ezdmb/6.9.0/gcc_64/bin":$PATH`

On Windows and Mac, use the Qt Framework install packages provided at <https://www.qt.io/>
