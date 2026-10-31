# Developer environment setup

The project requires Python 3.13 or later.

## Ubuntu Linux

1. Clone the repository if you have not already.
2. Run `bash linux/debian/setup-dev-environment.sh` from the repository root.
3. Activate the environment with `source .venv/bin/activate`.
4. Run the current source with `PYTHONPATH=src .venv/bin/python -m ezdmb`.

The setup script installs Python 3.13 on Ubuntu when needed, creates a virtual
environment, installs the project dependencies, and adds the Qt system
libraries required by the PySide6 Linux wheels.

## Windows

1. Install Python 3.13 or later, including the Python launcher: <https://www.python.org/downloads/windows/>
2. Clone the ezdmb repository.
3. Run `.\setup-dev-environment.ps1` from the repository root.
4. Set `$env:PYTHONPATH = "$PWD\src"` and run
   `.\.venv\Scripts\python.exe -m ezdmb`.

Debug messages are logged every time the display content updates. The content
update interval can be changed using `File > Settings`.

## Advanced install instructions / troubleshooting install

If the developer setup script does not work, verify that Python 3.13 or later
is installed and create the environment manually.

On Windows, run `py -3 -m venv .venv`, then
`.\.venv\Scripts\python.exe -m pip install --upgrade pip` and
`.\.venv\Scripts\python.exe -m pip install .`. Set `$env:PYTHONPATH = "$PWD\src"`
when launching to use the current source tree.

On Debian/Ubuntu, run `python3.13 -m venv .venv`, then
`.venv/bin/python -m pip install --upgrade pip` and
`.venv/bin/python -m pip install .`. Launch with
`PYTHONPATH=src .venv/bin/python -m ezdmb`. The Linux setup script also
installs the native Qt libraries needed to run the application.

### Generating resource files

Run `pyside6-rcc -o resources.py resources.qrc` from `src/ezdmb/View` to
regenerate the Qt resource module.
