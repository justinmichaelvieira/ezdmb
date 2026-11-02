[app]
title = ezdmb
project_dir = ..
input_file =
exec_directory = android/output
project_file = android/ezdmb_android.pyproject
icon = src/ezdmb/View/images/logo_192x192.png

[python]
python_path = 
packages = Nuitka==4.1.1
android_packages = buildozer==1.6.0,cython==0.29.33

[qt]
qml_files = 
excluded_qml_plugins = 
modules = Core,Gui,Widgets,Network,Pdf,PdfWidgets,Svg
plugins = 

[android]
wheel_pyside =
wheel_shiboken =
plugins =

[buildozer]
mode = debug
recipe_dir =
jars_dir =
ndk_path =
sdk_path =
local_libs =
arch = x86_64
