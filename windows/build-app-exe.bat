REM Build script  to create a Windows executable for the ezdmb application.

pyinstaller --onefile --name ezdmb --distpath ../ezdmb/dist ../ezdmb/__main__.py
