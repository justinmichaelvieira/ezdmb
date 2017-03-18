# ezdmb
A dead-simple digital menu board display and configuration, written in Python.  Engineered to be the simplest, cheapest, fastest way to get your menu to display on **any** tablet or computer.  Ridiculously user friendly, with one button configuration interface.

![Full ScreenMenu Image](/Images/354580462_orig.jpg)
![Configuration Window](/Images/ezdmb1.PNG)

## Prerequisites
Python 3 (https://www.python.org/downloads/)
Qt 5 (https://www.qt.io/)

## How to run
1. Clone or download all files.
2. Open a command line, and run `main.py` in the local ezdmb folder.  For example, on Windows I might run `python c:\Users\Justin\Documents\ezdmb\main.py`.

## Instructions / Basic Operation
The "Set New Image" button opens a file browser on the tablet/computer which will allow the user to select a different image.  On selection a config file, `dmb_config.json`, is written with the name of the selected menu board image.

## Coming Soon
- Bug fixes (ongoing)
- Installers for Windows, WinRT, Linux/android, iOS, MacOS
- "Premium" edition with backend API and multiple menu rendering options (import price list, HTML, etc)