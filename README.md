# ezdmb

![ezdmb logo](https://github.com/justinmichaelvieira/ezdmb/raw/master/readme_images/logo_crop.png "ezdmb logo")

A dead-simple digital menu board display and configuration.  Engineered to be the simplest, cheapest, fastest way to get your menu to display on **any** tablet or computer. Engineered for user-friendliness, with a simple, basic, configuration interface that easily allows rotation of images and quick configuration.

![Menu board display](https://github.com/justinmichaelvieira/ezdmb/raw/master/readme_images/sample1.png "Menu board display")

## Installing and running ezdmb on Windows

1. [Download the latest install zip.](https://github.com/justinmichaelvieira/ezdmb/releases/latest/download/ezdmb_install.zip)
2. Extract the entire zip file to any folder.
3. Double click install.bat.
4. Once the installer completes, you can launch the app using the Start Menu (Start > Run ezdmb)

## Basic Operation

- On startup, ezdmb opens the menu board in fullscreen and the Configuration window.
- Press `Esc` to exit the application. Press `o` while the fullscreen menu board is active to bring the Configuration window to the front.
- Use the system tray menu to show or minimize the Configuration and fullscreen windows. Choose **Minimize All** to hide the windows to the tray; double-click the tray icon to restore them.

## Configuration

The Configuration window includes the Settings controls:

- Enable or disable content rotation and set the interval in seconds.
- Add and remove content files. ezdmb displays images (`.jpg`, `.png`, `.gif`, `.bmp`, or `.ico`) and text files (`.txt`).
- Changes to the rotation settings and content list are saved automatically.
- Use **File > Export Content Bundle** to export the configuration and its content files as a ZIP bundle. Use **File > Import Content Bundle** to load a bundle.

The **File** menu also provides commands to minimize or show the Configuration and fullscreen windows, minimize all windows to the tray, and exit. The **Help** menu opens the Quickstart Guide and About window.

## Developer environment setups

[Windows and Ubuntu developer install scripts are available (useful if you want to do code updates)](DEVELOPERS.md)
