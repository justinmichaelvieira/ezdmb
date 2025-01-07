#!/bin/bash

# This is a cross-compilation script! Environments for x86_64-w64-mingw32-gcc and i686-w64-mingw32-gcc-win32 must
# be installed on the system, for this script to work.
#
# These commands *should* install the required, for ubuntu systems:
# sudo apt-get install gcc-multilib
# sudo apt-get install gcc-mingw-w64
# sudo apt install win-iconv-mingw-w64-dev
#
# Typically, x86_64-w64-mingw32-gcc and i686-w64-mingw32-gcc-win32 will install to /usr/bin/<compiler_name>.
#
# "upx" is also used to compress the binaries, after compilation. Upx can be installed with:
# sudo apt-get install upx 

mkdir -p build/

cd build/

which upx &> /dev/null &&
upx --best ezdmb-x64.exe &&
cp ezdmb-x64.exe ezdmb.exe &&
echo -e '\033[0;34m64bit Windows exe compiled and compressed successfully.\033[0m'

which upx &> /dev/null &&
upx --best ezdmb.exe &&
echo -e '\033[0;34m32bit Windows exe compiled and compressed successfully.\033[0m'

cd - > /dev/null

echo -e '\033[0;32mWindows exe build script completed.\033[0m'
