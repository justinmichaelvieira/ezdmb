# ezdmb AI Coding Agent Instructions

## Project Overview
ezdmb is a PyQt5-based digital menu board application for displaying rotating images/content on tablets or computers. The architecture follows an MVC pattern with clear separation between UI (View), business logic (Controller), and utilities.

## Architecture & Key Components

### Project Structure
```
src/ezdmb/
├── __main__.py                 # Application entry point; instantiates QApplication and windows
├── Controller/
│   ├── Configuration.py        # JSON config serialization/deserialization (QObject with signals)
│   └── LoggingUtility.py       # File + console logging setup
├── View/
│   ├── FullScreenWindow.py     # Full-screen display window for menu content
│   ├── ConfigDialog.py         # Settings/configuration UI
│   ├── PreviewWindow.py        # Configuration preview window
│   ├── AboutDialog.py          # About dialog
│   └── MenuContentViewUtility.py # Content rotation logic (QThread)
├── Utility/
│   └── ShortcutUtility.py      # Keyboard shortcuts (Esc to close, O to open config)
└── Resources/
    └── resources.qrc           # Qt resource file for embedded assets
```

### Data Flow
1. **Startup** (`__main__.py::main()`): Creates QApplication, instantiates Configuration, then creates three windows
2. **Configuration Loading** (`Configuration.py`): Reads/writes JSON from platform-specific appdata:
   - Windows: `%APPDATA%/ezdmb/dmb_config.json`
   - Linux: `~/.ezdmb/dmb_config.json`
3. **Content Rotation** (`MenuContentViewUtility.py`): QThread that cycles through images at intervals, emits signals to update display
4. **Configuration Updates**: ConfigDialog changes trigger `configUpdated` signal, which MenuContentViewUtility listens to via `onConfigUpdated` slot

### Signal/Slot Pattern
- **Configuration signals**: `configUpdated(dict)` - emitted when config saved
- **MenuContentViewUtility signals**: `contentUpdated(QPixmap)` - emitted when new image ready
- Connections use `@pyqtSlot` decorators for explicit type safety

## Development Workflow

### Running Locally
```powershell
# Windows dev environment setup (creates venv, installs deps)
./setup-dev-environment.ps1

# Run the app with debug output
python -m ezdmb
# or
py __main__.py
```

### Building for Distribution
**Windows executable** (from `windows/` directory):
```powershell
# Prompts for version, builds with PyInstaller, packages with Inno Setup
pyinstaller --onefile --name ezdmb --distpath artifacts ../src/ezdmb/__main__.py
```

**Linux AppImage/DEB** (from `linux/debian/` directory):
```bash
./build-linux-executable.sh
# Creates executable in overlay/opt/ezdmb/
```

### Testing
Existing test file: `Controller/LoggingUtility_test.py` (minimal coverage)
Pytest required but no tests currently in test suite - tests should follow existing pattern in LoggingUtility_test.py

## Project-Specific Patterns & Conventions

### Configuration Management
- All configuration stored in single JSON file via `Configuration.SaveConfig(rotate_bool, interval_seconds, content_paths[])`
- Configuration object is a QObject subclass to enable signal/slot communication
- Properties use verbose getter/setter pattern (not Python @property style) - see `Configuration.py` for example
- First-run defaults: rotate=True, interval="15", content_array=[]

### Widget Construction
- Programmatic widget creation (no .ui files) - layouts built in Python
- Custom stylesheet applied globally in `__main__.py::STYLESHEET` (dark Material Design colors)
- All windows created in `populateInstance()` function, not individual files

### Thread Safety
- MenuContentViewUtility extends QThread for content rotation
- Signals cross thread boundaries safely (Qt handles marshaling)
- File operations happen on main thread only

### Logging
- Centralized setup in `LoggingUtility.setupLogging()` 
- Logs to both `log.txt` (same directory as executable) and console
- DEBUG level for all messages
- Called once in `main()` after app start

### Keyboard Shortcuts
- Defined in `Utility/ShortcutUtility.py`
- Esc = close app (FullScreenWindow)
- O = show/bring config window to front

## Cross-Platform Considerations
- AppData paths handled conditionally: `os.getenv('APPDATA')` for Windows, `Path.home()` for Unix
- File operations use `os.path.join()` for portability
- Executable paths in build scripts differ (see `windows/build-app.bat` vs `linux/debian/build-linux-executable.sh`)

## Dependencies & Versions
- **PyQt5** >= 5.15.2 (core UI framework)
- **PyInstaller** (executable packaging)
- **black** (code formatting)
- **aqtinstall** (Qt framework management)
- Python >= 3.4 required

## Common Modifications
- **Add config option**: Add property to Configuration class, update JSON defaults in `__init__`, update `SaveConfig()` params
- **Add window**: Create in View/, instantiate in `populateInstance()`, connect signals if needed
- **Change rotation logic**: Modify `MenuContentViewUtility.run()` loop
- **Change styling**: Update `STYLESHEET` dict in `__main__.py`
- **Add keyboard shortcut**: Add function to `ShortcutUtility.py`, apply to window

## Notes for AI Agents
- Pylint is configured to disable certain checks - see `# pylint: disable` comments at file tops
- No automated tests currently exist beyond LoggingUtility_test.py
- Resource file (`resources.qrc`) must be compiled to Python with `pyrcc5` if modified
- Main app logic is simple; complexity is in Qt boilerplate rather than business logic
- Cross-platform builds require running scripts from specific directories (see `windows/` and `linux/debian/`)
