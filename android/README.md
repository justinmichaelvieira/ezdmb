# Android build and run

The Android entry point is the repository-root `main.py`, as required by
`pyside6-android-deploy`. It delegates to `ezdmb.android_entrypoint`; desktop
startup remains `python -m ezdmb`. Run deployment commands from the repository
root so the tool finds `main.py`. The deployment settings are in
[`pysidedeploy.spec`](./pysidedeploy.spec).

## Selected versions and requirements

The Android build configuration pins PySide6 6.12.0, matching the current
Qt for Python Android deployment documentation and the tested `--help` output
of `pyside6-android-deploy` 6.12.0.

| Component | Selected requirement |
|---|---|
| Host Python | Python 3.14; Qt's Android deployment tool accepts host Python 3.10–3.14 |
| Project Python floor | Python >=3.13, unchanged |
| Android Python | CPython 3.14.2 |
| PySide6 | 6.12.0 for the Android build |
| ARM64 ABI | `aarch64`, packaged as `arm64-v8a` |
| Emulator ABI | `x86_64`, used by the local AVD |
| JDK | JDK 21 or later; this host has OpenJDK 21.0.12.1 |
| Android NDK | r28c (`28.2.13676358`) |
| Android SDK | Platform API 36/build-tools 36.0.0 for the build; the Qt helper also installed API 35/build-tools 37.0.0 |
| Minimum Android API | 28, as required by the selected Qt Android deployment tool |

Use the [official deployment guide](https://doc.qt.io/qtforpython-6/deployment/deployment-pyside6-android-deploy.html)
for version updates. It documents the `pysidedeploy.spec` format, supported
architectures, Android wheel setup, and the requirement for a `main.py` entry
point.

## Linux build environment

Install a JDK 21 or newer and use a Python 3.14 virtual environment. For
example, on Debian/Ubuntu:

```bash
sudo apt install libssl-dev openjdk-21-jdk
export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
export PATH="$JAVA_HOME/bin:$PATH"

python3.14 -m venv "$HOME/.venvs/ezdmb-android"
source "$HOME/.venvs/ezdmb-android/bin/activate"
python -m pip install --upgrade pip
python -m pip install -r android/requirements-build.txt
python -m pip install jinja2 pkginfo tqdm "packaging==24.1"
```

`JAVA_HOME` must point to the JDK root; the Qt SDK manager will fail even when
`java` is on `PATH` if `JAVA_HOME` is unset. `buildozer` and Cython are
host-side deployment dependencies and are installed from the
`android_packages` entry in `pysidedeploy.spec`; they are not added to the
Android application's Python requirements.

Download the SDK, NDK, and target Python into the tool's user cache:

```bash
git clone --branch 6.12 https://code.qt.io/pyside/pyside-setup.git \
    /tmp/pyside-setup-6.12
python /tmp/pyside-setup-6.12/tools/cross_compile_android/main.py \
    --plat-name aarch64 \
    --download-only \
    --skip-update \
    --auto-accept-license
```

For the Qt 6.12 Java bindings, this host also installed the current Android
platform and build-tools packages:

```bash
"$ANDROID_SDK_ROOT/cmdline-tools/bin/sdkmanager" \
    --sdk_root="$ANDROID_SDK_ROOT" \
    "platforms;android-36" "build-tools;36.0.0"
```

The cache is `$HOME/.pyside6_android_deploy/`. Set the paths for later commands:

```bash
export ANDROID_SDK_ROOT="$HOME/.pyside6_android_deploy/android-sdk"
export ANDROID_NDK_HOME="$HOME/.pyside6_android_deploy/android-ndk/android-ndk-r28c"
export PATH="$ANDROID_SDK_ROOT/platform-tools:$PATH"
```

## PySide6 Android wheels

`pyside6-android-deploy` needs matching PySide6 and Shiboken Android wheels.
Qt publishes the open-source Android wheels in its public release archive.
Use `pip download` with an Android platform tag because the host is Linux:

```bash
mkdir -p android/wheels
python -m pip download --no-deps --only-binary=:all: \
    --dest android/wheels \
    --platform android_aarch64 \
    --python-version 3.14 \
    --implementation cp \
    --abi abi3 \
    https://download.qt.io/official_releases/QtForPython/pyside6/pyside6-6.12.0-6.12.0-cp310-abi3-android_aarch64.whl \
    https://download.qt.io/official_releases/QtForPython/shiboken6/shiboken6-6.12.0-6.12.0-cp310-abi3-android_aarch64.whl
```

To build for the x86_64 emulator instead, use `--platform android_x86_64` and
the filenames ending in `android_x86_64.whl`. Each wheel is about 90 MB. These
are public Qt 6.12.0 binary wheels; the commercial-license prompt from `qtpip`
does not apply when downloading the public URLs directly.

The build helper accepts `aarch64`, `arm64`, and `arm64-v8a` as names for the
same Android ARM64 ABI. All three require the matching
`android_aarch64` PySide6 and Shiboken wheels.

The downloads must match PySide6 6.12.0. Qt's current documentation also
describes cross-compiling wheels from the matching Qt for Android SDK. Install
Qt 6.12.0 with the Android kit and host tools, then run the
`tools/cross_compile_android/main.py` script from the matching `pyside-setup`
branch. Do not mix wheels and Qt SDKs from different Qt/PySide versions.

## Build a debug APK

Set these variables to the Android wheel files created or downloaded above:

```bash
export PYSIDE_ANDROID_WHEEL=/absolute/path/to/the/PySide6-6.12.0-Android-wheel.whl
export SHIBOKEN_ANDROID_WHEEL=/absolute/path/to/the/shiboken6-6.12.0-Android-wheel.whl
```

Then, from the repository root with the deployment virtual environment
activated and `JAVA_HOME` set:

```bash
python android/build.py --arch aarch64 \
    --wheel-pyside "$PYSIDE_ANDROID_WHEEL" \
    --wheel-shiboken "$SHIBOKEN_ANDROID_WHEEL" \
    --ndk-path "$ANDROID_NDK_HOME" \
    --sdk-path "$ANDROID_SDK_ROOT"
```

The configuration selects the `aarch64` ABI and debug mode. The APK is written
under `android/output/`. The Android project file restricts dependency
scanning to the Android entry point and its runtime dependencies. PDF and SVG
are declared under `TYPE_CHECKING` so the deploy scanner includes their
Android libraries without importing them at startup. Qt Multimedia and
WebEngine Widgets are deliberately excluded.

For emulator validation, download the `android_x86_64` wheel pair and build
with the supplied x86_64 project spec:

```bash
export PYSIDE_ANDROID_WHEEL="$PWD/android/wheels/pyside6-6.12.0-6.12.0-cp310-abi3-android_x86_64.whl"
export SHIBOKEN_ANDROID_WHEEL="$PWD/android/wheels/shiboken6-6.12.0-6.12.0-cp310-abi3-android_x86_64.whl"
python android/build.py --arch x86_64 \
    --wheel-pyside "$PYSIDE_ANDROID_WHEEL" \
    --wheel-shiboken "$SHIBOKEN_ANDROID_WHEEL" \
    --ndk-path "$ANDROID_NDK_HOME" \
    --sdk-path "$ANDROID_SDK_ROOT"
```

The generated `buildozer.spec` needs the `INTERNET` permission for Python URL
bundle imports; Qt's Network wheel metadata adds `ACCESS_NETWORK_STATE`, but
does not declare `INTERNET`. Remove the Multimedia defaults for `CAMERA`,
`RECORD_AUDIO`, and `BLUETOOTH` because this app only plays videos/audio. Keep
`MODIFY_AUDIO_SETTINGS`. [`build.py`](./build.py) invokes Qt's
`pyside6-android-deploy` entry point, adjusts the generated Buildozer spec for
API 36 and this app's minimum permissions, preserves the checked-in
deployment configuration, and verifies that a fresh APK was actually
produced. It expects `buildozer`, Cython, and the deployment tool to be in the
active build virtual environment.

For a release bundle, change `buildozer.mode` to `release`; the tool produces an
AAB. Configure release signing locally through the Android/Gradle signing
configuration. Do not put keystores, passwords, signing properties, or local
absolute paths in this repository.

## Install and inspect on Android

```bash
adb install -r android/output/ezdmb-0.1-arm64-v8a-debug.apk
adb logcat -c
adb logcat
```

For a one-step ARM64 build and install, connect and authorize the device, find
its serial with `adb devices -l`, then pass the matching ARM64 wheels and serial:

```bash
python android/build.py --arch arm64-v8a \
    --wheel-pyside "$PYSIDE_ANDROID_WHEEL" \
    --wheel-shiboken "$SHIBOKEN_ANDROID_WHEEL" \
    --ndk-path "$ANDROID_NDK_HOME" \
    --sdk-path "$ANDROID_SDK_ROOT" \
    --install --device-serial "$ADB_SERIAL"
```

`--install` installs the newly built APK with `adb install -r`; omit
`--device-serial` only when ADB has a single connected device. The device serial
option requires `--install`.

Check the generated APK's actual permissions before release:

```bash
"$ANDROID_SDK_ROOT/build-tools/37.0.0/aapt" dump permissions \
    android/output/<debug-apk-name>.apk
```

Qt's Network module metadata provides `ACCESS_NETWORK_STATE`; the build adds
`INTERNET` for URL bundle imports. SAF document picking does not require broad
shared-storage access. Qt's Android file dialog uses SAF, and Qt's
content-URI file engine copies selected bytes into app-private storage. The
build helper patches the python-for-android Qt activity to forward file-picker
results through Qt's activity-result handler and Android Back events to Qt.
Selected files are copied into
Qt's app-private `AppDataLocation`; bundles are staged privately, imported
assets remain in a unique private directory, and exports use the Android
document destination picker.

On an emulator or device, verify portrait/landscape resizing, menu startup,
background/foreground, Back navigation, file selection and persistence,
rotation modes and schedules, bundle import/export, and supported media. Run
`adb logcat` while testing for missing modules, permission errors, and
Python/Qt plugin errors. The Qt deployment tool supports `x86_64` as well; use
matching x86_64 wheels and change `buildozer.arch` only when an x86_64
emulator/device is available.

## Android behavior and limitations

- The app has one full-screen display window and an in-app Settings page. The
  Settings control is touch-sized; Android Back closes the schedule editor
  first, then returns from Settings to the display. No system tray, Esc/O
  shortcuts, or desktop menus are used.
- Bundle import/export results and errors are shown inline in Settings instead
  of opening a modal Qt dialog after Android's document picker returns.
- Rotation interval, None, named groups, daily/weekly/dated schedules, and the
  existing JSON configuration schema are retained. The mobile schedule editor
  edits one weekday or date and its half-hour block rows at a time.
- Local document URIs are copied to app-private storage before their paths are
  saved. Duplicate filenames are given distinct app-owned names. No
  `MANAGE_EXTERNAL_STORAGE` permission is requested.
- Qt WebEngine's documented platform list covers Windows, Linux, and macOS,
  not Android. Adding a web page is disabled with an explanation; existing web
  URLs show a visible display message. URL bundle imports still require the
  generated `INTERNET` permission.
- Qt Multimedia is excluded from this Android build. On Android 9/API 28,
  loading the Qt Multimedia module in the emulator caused a native crash in
  `JNI_OnLoad` (`QJniEnvironment::getJniEnv()`); video entries remain in the
  configuration but display a clear playback-unavailable fallback.
- PDF support depends on QtPdf and QtPdfWidgets being present in the selected
  Android wheel; otherwise the display reports that PDF viewing is unavailable.
- Presentations are rejected on Android because conversion currently depends
  on LibreOffice. Convert presentations to PDF before importing them.
- The app does not request device-owner/lock-task behavior or keep the screen
  awake. Android system navigation remains available.

## Validation status for this checkout

The current Qt for Python deployment guide and the installed
`pyside6-android-deploy --help` were checked for PySide6 6.12.0. The official
cross-build helper successfully downloaded NDK r28c, Android platform API 35,
build-tools 37.0.0, platform-tools, and CPython 3.14.2 for aarch64 after
`JAVA_HOME` was set.

Desktop regression checks pass with PySide6 6.12.0 in an isolated test
environment:

```bash
PYTHONPATH=src QT_QPA_PLATFORM=offscreen python -m pytest -q
cd src/ezdmb && ruff check
```

The full test suite reports 144 passed. Full Ruff checks, targeted `ty check`
for the Android implementation and build helper, and `git diff --check` pass.

The x86_64 debug APK was built with PySide6 6.12.0 using
`python android/build.py --arch x86_64 ...`, the public Qt Android
`cp310-abi3-android_x86_64` wheels, API 36/build-tools 36.0.0, NDK r28c, and
JDK 21. The APK is `output/ezdmb-0.1-x86_64-debug.apk` (173 MiB).
`aapt dump permissions` confirms only `ACCESS_NETWORK_STATE`, `INTERNET`, and
`MODIFY_AUDIO_SETTINGS`; no broad shared-storage permission is requested.

The final APK installed and ran on the Android 15/API 35 AOSP x86_64 AVD using
software CPU emulation (`/dev/kvm` is unavailable). Runtime checks covered the
display, Settings, touch scrolling, and schedule editor. The schedule editor
fits the emulator viewport; Android Back closes it before returning from
Settings to the display. A weekly time block was assigned and saved. The
Qt-native SAF picker opened; a sample image was copied from Downloads into
app-private storage, exported as a ZIP bundle to Downloads, and re-imported
successfully. The imported image and configuration persisted after restarting
the app. Cold startup is slow under TCG; Android System UI occasionally
reported an ANR while the large Qt Python bundle was being extracted, then
recovered without an app crash.

The x86_64 build was runtime-validated on API 35. The ARM64 APK was installed
and tested on a Samsung Galaxy Tab S9 (SM-X810, Android 16/API 36). A valid
bundle import reproduced a native Qt abort after the Android document picker
returned. Import/export feedback now appears inline in Settings instead of
opening a modal dialog; the same controlled bundle imported successfully and
the app remained running. The tablet's original configuration was restored
after testing. The Samsung SM-G960U1 (Android 10/API 29), API 28, PDF, and video
playback remain unverified. Qt Multimedia remains excluded after its earlier
native `JNI_OnLoad` crash on the API 28 emulator; video entries show the
documented unavailable fallback.
