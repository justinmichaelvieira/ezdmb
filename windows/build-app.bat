REM Builds Windows executable and updates version files for the ezdmb application.

set /p "VERSION=Enter version: "

(
  echo $VERSION
) > %~dp0\docker\artifacts\.version

if not exist "dist\" mkdir dist
pyinstaller --onefile --name ezdmb --distpath docker\artifacts ..\ezdmb\__main__.py
xcopy /s dist\ezdmb.exe docker\artifacts\ezdmb.exe
