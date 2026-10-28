import os
import re
import tempfile
import zipfile
from copy import deepcopy
from html import escape
from http.client import HTTPException
from pathlib import Path
from shutil import copyfile, copyfileobj, rmtree
from urllib.parse import urlparse
from urllib.request import urlopen

from PySide6.QtCore import SignalInstance
from PySide6.QtWidgets import QDialog, QFileDialog, QInputDialog

from ezdmb.Controller.configuration import configuration
from ezdmb.Utility.path_utility import get_appdata_path
from ezdmb.View.simple_text_dialog import simple_text_dialog


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
    with zipfile.ZipFile(zip_file, "r") as zip_ref:
        zip_ref.extractall(extract_dir)


def _show_import_error(message: str, testing: bool):
    if not testing:
        simple_text_dialog("Import Failed", message).exec()


def _import_bundle_archive(
    zip_file: Path | str,
    trigger_settings_ui_update: SignalInstance,
    configuration: configuration,
    testing=False,
):
    if not zipfile.is_zipfile(zip_file):
        _show_import_error("The selected file is not a valid ZIP bundle.", testing)
        return

    # Create a folder for extraction
    extract_folder = os.path.join(get_appdata_path(), "ezdmb_bundle")
    if os.path.exists(extract_folder):
        rmtree(extract_folder)

    Path(extract_folder).mkdir(parents=True, exist_ok=False)

    # Extract the zip file to the folder
    try:
        unzip_dir(zip_file, extract_folder)
    except (OSError, RuntimeError, zipfile.BadZipFile) as error:
        rmtree(extract_folder, ignore_errors=True)
        _show_import_error(
            f"Could not extract the bundle: {escape(str(error))}",
            testing,
        )
        return

    # Update the configuration with the extracted files
    new_config_path = os.path.join(extract_folder, "dmb_config.json")
    if not os.path.exists(new_config_path):
        _show_import_error(
            "The bundle does not contain a dmb_config.json file.",
            testing,
        )
        return

    regex = re.compile("(.*jpg$)|(.*png$)|(.*gif$)|(.*bmp$)|(.*ico$)|(.*txt$)")
    content_files = [
        file_path
        for file_path in Path(extract_folder).glob("*")
        if file_path.is_file() and regex.match(str(file_path))
    ]

    configuration.load_from_file(new_config_path)
    extracted_files = {
        file_path.name.casefold(): str(file_path) for file_path in content_files
    }
    content_groups = deepcopy(configuration.ContentGroups)
    for group in content_groups:
        group["content"] = [
            extracted_files[Path(content_path).name.casefold()]
            for content_path in group["content"]
        ]

    configuration.save_config(
        configuration.get_rotate_content(),
        configuration.get_rotate_content_time(),
        content_files,
        configuration.get_config_path(),
        TimeBlocks=configuration.TimeBlocks,
        ContentGroups=content_groups,
        RotationMode=configuration.RotationMode,
    )

    # TODO: refresh ui with new values
    trigger_settings_ui_update.emit()

    if not testing:
        simple_text_dialog(
            "Import Successful",
            "The bundle has been successfully imported.",
        ).exec()


def import_bundle(
    trigger_settings_ui_update: SignalInstance,
    configuration: configuration,
    testing=False,
):
    """Select a zip bundle and extract it to the application directory, updating the configuration accordingly."""

    zip_file = QFileDialog.getOpenFileName(
        None,
        "Select Zip Bundle",
        filter="Zip Files (*.zip)",
    )[0]
    if not zip_file:
        return

    _import_bundle_archive(
        zip_file,
        trigger_settings_ui_update,
        configuration,
        testing,
    )


def import_bundle_from_url(
    trigger_settings_ui_update: SignalInstance,
    configuration: configuration,
    testing=False,
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
            )
            return

        _import_bundle_archive(
            zip_file,
            trigger_settings_ui_update,
            configuration,
            testing,
        )


def export_bundle(configuration: configuration, testing=False):
    """Select a directory and save it as a zip file in a temporary location."""

    # Open a dialog to select a directory
    output_dir = QFileDialog.getExistingDirectory(None, "Select Directory to save zip bundle")
    if not output_dir:
        return  # User canceled the dialog

    # Create a temporary folder for the files to zip
    with tempfile.TemporaryDirectory() as temp_folder:
        # Copy the config file and content files to the temporary folder
        copyfile(configuration.ConfigPath, os.path.join(temp_folder, "dmb_config.json"))
        for content_file in configuration.ContentArray:
            copyfile(content_file, os.path.join(temp_folder, Path(content_file).name))

        # Zip the directory
        zip_dir(temp_folder, "ezdmb_bundle.zip")

        # Copy the zip bundle to the selected output directory
        copyfile("ezdmb_bundle.zip", os.path.join(output_dir, "ezdmb_bundle.zip"))

    if not testing:
        simple_text_dialog(
            "Export Successful",
            f"""The bundle has been successfully exported to: {Path(output_dir) / 'ezdmb_bundle.zip'}""",
        ).exec()
