import os
import re
import tempfile
import zipfile
from pathlib import Path
from shutil import copyfile, rmtree

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog

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


def import_bundle(trigger_settings_ui_update: Signal, configuration: configuration, testing=False):
    """Select a zip bundle and extract it to the application directory, updating the configuration accordingly."""

    # Open a dialog to select a zip file
    zip_file = QFileDialog.getOpenFileName(None, "Select Zip Bundle", filter="Zip Files (*.zip)")[0]
    if not zip_file:
        return  # User canceled the dialog

    # Create a folder for extraction
    extract_folder = os.path.join(get_appdata_path(), "ezdmb_bundle")
    if os.path.exists(extract_folder):
        rmtree(extract_folder)

    Path(extract_folder).mkdir(parents=True, exist_ok=False)

    # Extract the zip file to the folder
    unzip_dir(zip_file, extract_folder)

    # Update the configuration with the extracted files
    new_config_path = os.path.join(extract_folder, "dmb_config.json")
    if os.path.exists(new_config_path):
        regex = re.compile('(.*jpg$)|(.*png$)|(.*gif$)|(.*bmp$)|(.*ico$)|(.*txt$)') 
        content_files = [f for f in Path(extract_folder).glob("*") if regex.match(str(f))]

        configuration.load_from_file(new_config_path)

        configuration.save_config(
            configuration.get_rotate_content(),
            configuration.get_rotate_content_time(),
            content_files,
            configuration.get_config_path(),
        )

        # TODO: refresh ui with new values
        trigger_settings_ui_update.emit()

        if not testing:
            simple_text_dialog(
                "Export Successful",
                "The bundle has been successfully imported.",
            ).exec()


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
