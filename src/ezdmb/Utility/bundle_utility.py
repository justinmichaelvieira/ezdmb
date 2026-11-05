import json
import stat
import tempfile
import zipfile
from collections.abc import Callable
from copy import deepcopy
from html import escape
from http.client import HTTPException
from pathlib import Path, PurePosixPath
from shutil import copyfile, copyfileobj, rmtree
from typing import Protocol
from urllib.parse import urlparse
from urllib.request import urlopen
from uuid import uuid4

from PySide6.QtCore import SignalInstance
from PySide6.QtWidgets import QDialog, QFileDialog, QInputDialog

from ezdmb.Controller.configuration import (
    configuration,
    default_content_groups,
)
from ezdmb.Utility.media_utility import (
    PRESENTATION_FILE_EXTENSIONS,
    get_content_type,
    is_web_url,
)
from ezdmb.Utility.path_utility import get_appdata_path, is_android
from ezdmb.View.simple_text_dialog import simple_text_dialog


class bundle_storage_adapter(Protocol):
    def pick_bundle_file(self) -> Path | None: ...

    def release_staged_bundle(self, path: str | Path) -> None: ...

    def save_bundle(self, source: str | Path) -> bool: ...


# Source - https://stackoverflow.com/a/68817065
# Posted by JD Solanki, modified by community. See post 'Timeline' for change history
# Retrieved 2026-09-06, License - CC BY-SA 4.0
def zip_dir(dir: Path | str, output_filename: Path | str):
    """Zip the provided directory without navigating to that directory using `pathlib` module"""

    # Convert to Path object
    dir = Path(dir)

    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for entry in dir.rglob("*"):
            zip_file.write(entry, entry.relative_to(dir))


# Source - https://stackoverflow.com/a/3451150
# Posted by Rahul, modified by community. See post 'Timeline' for change history
# Retrieved 2026-09-06, License - CC BY-SA 4.0
def unzip_dir(zip_file: Path | str, extract_dir: Path | str):
    root = Path(extract_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        for entry in zip_ref.infolist():
            normalized_name = entry.filename.replace("\\", "/")
            relative_path = PurePosixPath(normalized_name)
            if (
                relative_path.is_absolute()
                or any(part == ".." for part in relative_path.parts)
                or (relative_path.parts and relative_path.parts[0].endswith(":"))
            ):
                raise ValueError(
                    f"Bundle contains an unsafe archive path: {entry.filename}"
                )
            if not relative_path.parts:
                continue

            destination = root.joinpath(*relative_path.parts)
            if not destination.resolve().is_relative_to(root):
                raise ValueError(
                    f"Bundle contains an unsafe archive path: {entry.filename}"
                )
            file_mode = entry.external_attr >> 16
            if stat.S_ISLNK(file_mode):
                raise ValueError(
                    f"Bundle contains an unsupported symbolic link: {entry.filename}"
                )
            if entry.is_dir():
                destination.mkdir(parents=True, exist_ok=True)
                continue

            destination.parent.mkdir(parents=True, exist_ok=True)
            with (
                zip_ref.open(entry, "r") as source,
                destination.open("wb") as target,
            ):
                copyfileobj(source, target)


def _show_import_error(
    message: str,
    testing: bool,
    status_callback: Callable[[str], None] | None = None,
):
    if testing:
        return
    if status_callback is not None:
        status_callback(message)
    else:
        simple_text_dialog("Import Failed", message).exec()


def _show_export_error(
    message: str,
    testing: bool,
    status_callback: Callable[[str], None] | None = None,
):
    if testing:
        return
    if status_callback is not None:
        status_callback(message)
    else:
        simple_text_dialog("Export Failed", message).exec()


def _import_bundle_archive(
    zip_file: Path | str,
    trigger_settings_ui_update: SignalInstance,
    configuration: configuration,
    testing=False,
    status_callback: Callable[[str], None] | None = None,
):
    if not zipfile.is_zipfile(zip_file):
        _show_import_error(
            "The selected file is not a valid ZIP bundle.",
            testing,
            status_callback,
        )
        return False

    extract_folder = (
        Path(get_appdata_path())
        / "content"
        / "imports"
        / uuid4().hex
    )
    try:
        extract_folder.mkdir(parents=True, exist_ok=False)
        unzip_dir(zip_file, extract_folder)
        new_config_path = extract_folder / "dmb_config.json"
        if not new_config_path.is_file():
            raise ValueError(
                "The bundle does not contain a dmb_config.json file."
            )

        with new_config_path.open("r", encoding="utf-8") as config_file:
            imported_data = json.load(config_file)
        if not isinstance(imported_data, dict):
            raise TypeError("The bundle configuration must be a JSON object.")

        imported_groups = imported_data.get("content_groups")
        if not isinstance(imported_groups, list) or not imported_groups:
            imported_groups = [
                {"content": imported_data.get("imported_content", [])}
            ]
        if is_android():
            for group in imported_groups:
                if not isinstance(group, dict):
                    raise TypeError(
                        "The bundle contains an invalid content group."
                    )
                group_content = group.get("content", [])
                if not isinstance(group_content, list):
                    raise TypeError(
                        "The bundle contains an invalid content group."
                    )
                if any(
                    Path(str(content_path)).suffix.casefold()
                    in PRESENTATION_FILE_EXTENSIONS
                    for content_path in group_content
                    if not is_web_url(str(content_path))
                ):
                    raise ValueError(
                        "This bundle contains PowerPoint presentations, which "
                        "cannot be rendered on Android. Convert them to PDF "
                        "and import again."
                    )

        configuration.load_from_file(new_config_path)
        content_groups = deepcopy(configuration.ContentGroups)

        content_files = sorted(
            (
                file_path
                for file_path in extract_folder.rglob("*")
                if file_path.is_file()
                and file_path != new_config_path
                and get_content_type(file_path.name) is not None
            ),
            key=lambda file_path: str(file_path).casefold(),
        )
        files_by_name: dict[str, list[Path]] = {}
        for file_path in content_files:
            files_by_name.setdefault(file_path.name.casefold(), []).append(
                file_path
            )

        for group in content_groups:
            resolved_content = []
            for content_path in group["content"]:
                if is_web_url(content_path):
                    resolved_content.append(content_path)
                    continue
                matching_files = files_by_name.get(
                    Path(content_path).name.casefold(),
                    [],
                )
                if not matching_files:
                    raise FileNotFoundError(
                        f"The bundle is missing content file: "
                        f"{Path(content_path).name}"
                    )
                if len(matching_files) > 1:
                    raise ValueError(
                        f"The bundle contains ambiguous duplicate filenames: "
                        f"{Path(content_path).name}"
                    )
                resolved_content.append(str(matching_files[0]))
            group["content"] = resolved_content

        configuration.save_config(
            configuration.get_rotate_content(),
            configuration.get_rotate_content_time(),
            [
                content
                for group in content_groups
                for content in group["content"]
            ],
            configuration.get_config_path(),
            TimeBlocks=configuration.TimeBlocks,
            ContentGroups=content_groups,
            RotationMode=configuration.RotationMode,
        )
    except (
        OSError,
        RuntimeError,
        ValueError,
        KeyError,
        TypeError,
        zipfile.BadZipFile,
    ) as error:
        rmtree(extract_folder, ignore_errors=True)
        _show_import_error(
            f"Could not import the bundle: {escape(str(error))}",
            testing,
            status_callback,
        )
        return False

    trigger_settings_ui_update.emit()

    if not testing:
        message = "The bundle has been successfully imported."
        if status_callback is not None:
            status_callback(message)
        else:
            simple_text_dialog("Import Successful", message).exec()
    return True


def import_bundle(
    trigger_settings_ui_update: SignalInstance,
    configuration: configuration,
    testing=False,
    storage_adapter: bundle_storage_adapter | None = None,
    status_callback: Callable[[str], None] | None = None,
):
    """Select a zip bundle and extract it to the application directory, updating the configuration accordingly."""

    if storage_adapter is None:
        zip_file = QFileDialog.getOpenFileName(
            None,
            "Select Zip Bundle",
            filter="Zip Files (*.zip)",
        )[0]
    else:
        try:
            zip_file = storage_adapter.pick_bundle_file()
        except (OSError, RuntimeError, ValueError) as error:
            _show_import_error(
                f"Could not open the selected bundle: {escape(str(error))}",
                testing,
                status_callback,
            )
            return False
    if not zip_file:
        return False

    try:
        return _import_bundle_archive(
            zip_file,
            trigger_settings_ui_update,
            configuration,
            testing,
            status_callback,
        )
    finally:
        if storage_adapter is not None:
            storage_adapter.release_staged_bundle(zip_file)


def import_bundle_from_url(
    trigger_settings_ui_update: SignalInstance,
    configuration: configuration,
    testing=False,
    status_callback: Callable[[str], None] | None = None,
):
    """Download and import a zip bundle from an HTTP or HTTPS URL."""

    url_dialog = QInputDialog()
    url_dialog.setWindowTitle("Import Bundle From URL")
    url_dialog.setLabelText("URL:")
    url_dialog.setInputMode(QInputDialog.InputMode.TextInput)
    url_dialog.setOkButtonText("Import")
    url_dialog.setCancelButtonText("Cancel")

    if url_dialog.exec() != QDialog.DialogCode.Accepted:
        return

    bundle_url = url_dialog.textValue().strip()
    try:
        parsed_url = urlparse(bundle_url)
        valid_url = (
            parsed_url.scheme in ("http", "https") and parsed_url.hostname is not None
        )
    except ValueError:
        valid_url = False

    if not valid_url:
        _show_import_error(
            "Please enter a valid HTTP or HTTPS bundle URL.",
            testing,
            status_callback,
        )
        return

    with tempfile.TemporaryDirectory() as temp_folder:
        zip_file = Path(temp_folder) / "bundle.zip"
        try:
            with urlopen(bundle_url, timeout=30) as response, zip_file.open(
                "wb"
            ) as output_file:
                copyfileobj(response, output_file)
        except (HTTPException, OSError, ValueError) as error:
            _show_import_error(
                f"Could not download the bundle: {escape(str(error))}",
                testing,
                status_callback,
            )
            return

        _import_bundle_archive(
            zip_file,
            trigger_settings_ui_update,
            configuration,
            testing,
            status_callback,
        )


def _unique_bundle_name(name: str, used_names: set[str]) -> str:
    original = Path(name)
    stem = original.stem or "content"
    suffix = original.suffix
    candidate = name
    index = 2
    while candidate.casefold() in used_names:
        candidate = f"{stem} ({index}){suffix}"
        index += 1
    used_names.add(candidate.casefold())
    return candidate


def _create_bundle_archive(configuration: configuration, archive_path: Path):
    content_groups = getattr(configuration, "ContentGroups", None)
    if not isinstance(content_groups, list) or not content_groups:
        content_groups = default_content_groups(
            getattr(configuration, "ContentArray", [])
        )
    content_groups = deepcopy(content_groups)

    config_data = getattr(configuration, "Data", None)
    if not isinstance(config_data, dict):
        with open(configuration.ConfigPath, encoding="utf-8") as config_file:
            config_data = json.load(config_file)
    else:
        config_data = deepcopy(config_data)

    with tempfile.TemporaryDirectory() as temp_folder:
        bundle_directory = Path(temp_folder)
        copied_sources: dict[str, str] = {}
        used_names: set[str] = set()

        for group in content_groups:
            bundled_content = []
            for content in group["content"]:
                content_path = str(content)
                if is_web_url(content_path):
                    bundled_content.append(content_path)
                    continue

                source_path = Path(content_path)
                if not source_path.is_file():
                    raise FileNotFoundError(
                        f"Content file does not exist: {source_path}"
                    )
                source_key = str(source_path.resolve())
                bundle_name = copied_sources.get(source_key)
                if bundle_name is None:
                    bundle_name = _unique_bundle_name(
                        source_path.name,
                        used_names,
                    )
                    copyfile(source_path, bundle_directory / bundle_name)
                    copied_sources[source_key] = bundle_name
                bundled_content.append(bundle_name)
            group["content"] = bundled_content

        config_data["content_groups"] = content_groups
        config_data["imported_content"] = [
            content
            for group in content_groups
            for content in group["content"]
        ]
        with (bundle_directory / "dmb_config.json").open(
            "w",
            encoding="utf-8",
        ) as config_file:
            json.dump(config_data, config_file)

        zip_dir(bundle_directory, archive_path)


def export_bundle(
    configuration: configuration,
    testing=False,
    storage_adapter: bundle_storage_adapter | None = None,
    status_callback: Callable[[str], None] | None = None,
):
    """Create a ZIP bundle and save it to a desktop directory or SAF document."""

    output_dir = ""
    if storage_adapter is None:
        output_dir = QFileDialog.getExistingDirectory(
            None,
            "Select Directory to save zip bundle",
        )
        if not output_dir:
            return False

    with tempfile.TemporaryDirectory() as temp_folder:
        archive_path = Path(temp_folder) / "ezdmb_bundle.zip"
        try:
            _create_bundle_archive(configuration, archive_path)
            if storage_adapter is not None:
                if not storage_adapter.save_bundle(archive_path):
                    return False
            else:
                copyfile(
                    archive_path,
                    Path(output_dir) / archive_path.name,
                )
        except (OSError, RuntimeError, ValueError, TypeError) as error:
            _show_export_error(
                f"Could not export the bundle: {escape(str(error))}",
                testing,
                status_callback,
            )
            return False

    if not testing:
        message = (
            "The bundle has been successfully saved."
            if storage_adapter is not None
            else f"The bundle has been successfully exported to: "
            f"{Path(output_dir) / 'ezdmb_bundle.zip'}"
        )
        if status_callback is not None:
            status_callback(message)
        else:
            simple_text_dialog("Export Successful", message).exec()
    return True
