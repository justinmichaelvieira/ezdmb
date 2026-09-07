import zipfile
from pathlib import Path
from shutil import copyfile
from tempfile import mkdtemp

from PySide6.QtWidgets import QFileDialog

from ezdmb.Controller.configuration import configuration


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
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

def select_dir_and_save_bundle(configuration: configuration):
    """Select a directory and save it as a zip file in a temporary location."""

    # Open a dialog to select a directory
    output_dir = QFileDialog.getExistingDirectory(None, "Select Directory to Zip")
    if not output_dir:
        return  # User canceled the dialog

    # Create a temporary folder for the files to zip
    temp_folder = Path(mkdtemp())

    # Copy the config file and content files to the temporary folder
    copyfile(configuration.ConfigPath, temp_folder / "dmb_config.json")
    for content_file in configuration.ContentArray:
        copyfile(content_file, temp_folder)

    # Zip the directory
    zip_dir(temp_folder, "ezdmb_bundle.zip")

    # Copy the zip bundle to the selected output directory
    copyfile("ezdmb_bundle.zip", Path(output_dir) / "ezdmb_bundle.zip")
