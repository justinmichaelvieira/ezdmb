"""Build ezdmb Android packages with Qt's PySide6 deployment tool."""

import argparse
import importlib
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ANDROID_PERMISSIONS = (
    "android.permission.ACCESS_NETWORK_STATE",
    "android.permission.INTERNET",
    "android.permission.MODIFY_AUDIO_SETTINGS",
)


def _patch_buildozer_spec(buildozer_spec: Path):
    content = buildozer_spec.read_text(encoding="utf-8")
    values = {
        "android.api": "36",
        "requirements": "python3,shiboken6,PySide6,ezdmb",
        "android.permissions": ", ".join(ANDROID_PERMISSIONS),
    }
    include_extensions_pattern = re.compile(
        r"(?m)^(source\.include_exts\s*=\s*.*)$"
    )
    content, replacements = include_extensions_pattern.subn(
        r"\1\nsource.include_patterns = src/ezdmb/**",
        content,
        count=1,
    )
    if replacements != 1:
        raise RuntimeError(
            f"Could not configure Android Python package files in "
            f"{buildozer_spec}."
        )

    for key, value in values.items():
        pattern = re.compile(rf"(?m)^({re.escape(key)}\s*=\s*).*$")
        content, replacements = pattern.subn(
            rf"\g<1>{value}",
            content,
            count=1,
        )
        if replacements != 1:
            raise RuntimeError(
                f"Expected exactly one {key} entry in {buildozer_spec}."
            )
    buildozer_spec.write_text(content, encoding="utf-8")


def _write_ezdmb_recipe(recipes_directory: Path, source_package: Path):
    recipe_directory = recipes_directory / "ezdmb"
    recipe_directory.mkdir(parents=True, exist_ok=True)
    recipe_source = f'''"""Install ezdmb's src-layout package into Android Python."""

from pathlib import Path
from shutil import copytree, ignore_patterns

from pythonforandroid.logger import info
from pythonforandroid.recipe import PythonRecipe


class EzdmbRecipe(PythonRecipe):
    name = "ezdmb"
    version = "1.1.0"
    site_packages_name = "ezdmb"
    depends = ["python3"]

    def _patch_qt_activity_callbacks(self):
        activity_source = (
            Path(self.ctx.bootstrap.build_dir)
            / "src"
            / "main"
            / "java"
            / "org"
            / "kivy"
            / "android"
            / "PythonActivity.java"
        )
        content = activity_source.read_text(encoding="utf-8")
        method_start = (
            "    protected void onActivityResult("
            "int requestCode, int resultCode, Intent intent) {{\\n"
        )
        super_call = (
            "        super.onActivityResult(requestCode, resultCode, intent);\\n"
        )
        on_key_down_method = (
            "public boolean onKeyDown(int keyCode, KeyEvent event) {{"
        )
        back_call = (
            "\\n        if (keyCode == KeyEvent.KEYCODE_BACK && "
            "super.onKeyDown(keyCode, event)) {{\\n"
            "            return true;\\n"
            "        }}\\n"
        )
        changed = False
        if super_call not in content:
            if content.count(method_start) != 1:
                raise RuntimeError(
                    f"Could not patch Activity-result forwarding in "
                    f"{{activity_source}}."
                )
            content = content.replace(
                method_start,
                method_start + super_call,
                count=1,
            )
            changed = True
        if (
            "keyCode == KeyEvent.KEYCODE_BACK && "
            "super.onKeyDown(keyCode, event)"
        ) not in content:
            if content.count(on_key_down_method) != 1:
                raise RuntimeError(
                    f"Could not patch Android Back forwarding in "
                    f"{{activity_source}}."
                )
            content = content.replace(
                on_key_down_method,
                on_key_down_method + back_call,
                count=1,
            )
            changed = True
        if changed:
            activity_source.write_text(content, encoding="utf-8")
            info("Patched Qt Activity to forward SAF and Back events")

    def build_arch(self, arch):
        source = Path({str(source_package.resolve())!r})
        destination = Path(self.ctx.get_python_install_dir(arch.arch)) / "ezdmb"
        info(f"Copying ezdmb Python package from {{source}} to {{destination}}")
        copytree(
            source,
            destination,
            ignore=ignore_patterns("__pycache__", "*_test.py"),
        )
        self._patch_qt_activity_callbacks()


recipe = EzdmbRecipe()
'''
    (recipe_directory / "__init__.py").write_text(
        recipe_source,
        encoding="utf-8",
    )


def _install_apk(apk_path: Path, sdk_path: Path, device_serial: str | None):
    adb_name = "adb.exe" if os.name == "nt" else "adb"
    adb_path = sdk_path / "platform-tools" / adb_name
    if not adb_path.is_file():
        adb_from_path = shutil.which("adb")
        if not adb_from_path:
            raise FileNotFoundError(
                "Android Debug Bridge was not found in the SDK or PATH."
            )
        adb_path = Path(adb_from_path)

    command = [str(adb_path)]
    if device_serial:
        command.extend(("-s", device_serial))
    command.extend(("install", "-r", str(apk_path.resolve())))
    subprocess.run(command, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Build a PySide6 Android debug APK or release AAB."
    )
    parser.add_argument(
        "--arch",
        choices=("aarch64", "arm64", "arm64-v8a", "x86_64"),
        default="aarch64",
        help="Target architecture; arm64 and arm64-v8a are aliases for aarch64.",
    )
    parser.add_argument("--wheel-pyside", type=Path, required=True)
    parser.add_argument("--wheel-shiboken", type=Path, required=True)
    parser.add_argument("--sdk-path", type=Path)
    parser.add_argument("--ndk-path", type=Path)
    parser.add_argument(
        "--install",
        action="store_true",
        help="Install the newly built APK on a connected Android device.",
    )
    parser.add_argument(
        "--device-serial",
        help="ADB serial of the target device; requires --install.",
    )
    parser.add_argument("--keep-deployment-files", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.device_serial and not args.install:
        parser.error("--device-serial requires --install.")
    if args.install and args.dry_run:
        parser.error("--install cannot be used with --dry-run.")

    arch = (
        "aarch64"
        if args.arch in ("aarch64", "arm64", "arm64-v8a")
        else args.arch
    )
    if sys.prefix == sys.base_prefix:
        raise SystemExit(
            "Run this script from an activated Python virtual environment."
        )
    os.environ.setdefault("VIRTUAL_ENV", sys.prefix)
    os.environ["PATH"] = (
        f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}"
    )

    repository_root = Path(__file__).resolve().parents[1]
    os.chdir(repository_root)
    android_cache = Path.home() / ".pyside6_android_deploy"
    sdk_path = args.sdk_path or Path(
        os.environ.get(
            "ANDROID_SDK_ROOT",
            android_cache / "android-sdk",
        )
    )
    ndk_path = args.ndk_path or Path(
        os.environ.get(
            "ANDROID_NDK_HOME",
            android_cache / "android-ndk" / "android-ndk-r28c",
        )
    )
    os.environ["ANDROID_HOME"] = str(sdk_path)
    os.environ["ANDROID_SDK_ROOT"] = str(sdk_path)
    os.environ["ANDROID_NDK_HOME"] = str(ndk_path)
    os.environ["ANDROID_NDK_ROOT"] = str(ndk_path)

    deployment_environment = Path(sys.executable).parent.parent
    scripts_directory = (
        deployment_environment
        / "lib"
        / f"python{sys.version_info.major}.{sys.version_info.minor}"
        / "site-packages"
        / "PySide6"
        / "scripts"
    )
    if not scripts_directory.is_dir():
        raise FileNotFoundError(
            f"PySide6 deployment scripts were not found in {scripts_directory}."
        )
    sys.path.insert(0, str(scripts_directory))

    deploy = importlib.import_module("android_deploy").main
    Buildozer = importlib.import_module(
        "deploy_lib.android.buildozer"
    ).Buildozer

    if arch == "aarch64":
        config_file = repository_root / "android" / "pysidedeploy.spec"
    else:
        config_file = (
            repository_root / "android" / "pysidedeploy-x86_64.spec"
        )
    if not args.wheel_pyside.is_file():
        raise FileNotFoundError(args.wheel_pyside)
    if not args.wheel_shiboken.is_file():
        raise FileNotFoundError(args.wheel_shiboken)
    wheel_suffix = f"android_{arch}.whl"
    for wheel_path in (args.wheel_pyside, args.wheel_shiboken):
        if not wheel_path.name.endswith(wheel_suffix):
            raise ValueError(
                f"{wheel_path} does not match --arch {args.arch}; "
                f"expected a wheel ending in {wheel_suffix}."
            )

    original_config = config_file.read_bytes()
    original_create_executable = Buildozer.create_executable
    recipes_directory = repository_root / "deployment" / "recipes"
    source_package = repository_root / "src" / "ezdmb"

    def create_executable(mode):
        if not args.dry_run:
            _write_ezdmb_recipe(recipes_directory, source_package)
            _patch_buildozer_spec(repository_root / "buildozer.spec")
        return original_create_executable(mode)

    Buildozer.create_executable = staticmethod(create_executable)
    started_at = time.time()
    try:
        deploy(
            name="ezdmb",
            pyside_wheel=args.wheel_pyside.resolve(),
            shiboken_wheel=args.wheel_shiboken.resolve(),
            ndk_path=ndk_path.resolve(),
            sdk_path=sdk_path.resolve(),
            config_file=config_file,
            loglevel=logging.INFO,
            dry_run=args.dry_run,
            keep_deployment_files=args.keep_deployment_files,
            force=True,
        )
    finally:
        config_file.write_bytes(original_config)
        Buildozer.create_executable = staticmethod(
            original_create_executable
        )

    if not args.dry_run:
        output_directory = repository_root / "android" / "output"
        new_apks = [
            path
            for path in output_directory.glob("*.apk")
            if path.stat().st_mtime >= started_at - 2
        ]
        if not new_apks:
            raise SystemExit(
                "The deployment tool returned without creating a new APK."
            )
        latest_apk = max(new_apks, key=lambda path: path.stat().st_mtime)
        print(f"Android APK created: {latest_apk}")
        if args.install:
            _install_apk(latest_apk, sdk_path, args.device_serial)


if __name__ == "__main__":
    main()
