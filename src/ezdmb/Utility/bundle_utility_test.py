import os
import tempfile
import unittest
import zipfile

import pytest

from ezdmb.Utility.bundle_utility import unzip_dir, zip_dir


class bundle_utility_test(unittest.TestCase):
    
    def test_zip_dir_preserves_files_and_relative_paths(self):
        temp_dir = tempfile.TemporaryDirectory()
        source_dir = os.path.join(temp_dir.name, "source")
        nested_dir = os.path.join(source_dir, "nested")
        os.makedirs(nested_dir, exist_ok=True)
        with open(os.path.join(source_dir, "menu.txt"), "w", encoding="utf-8") as f:
            f.write("daily menu")
        with open(os.path.join(nested_dir, "special.txt"), "w", encoding="utf-8") as f:
            f.write("today's special")
        archive_path = os.path.join(temp_dir.name, "menu.zip")

        zip_dir(source_dir, archive_path)

        with zipfile.ZipFile(archive_path) as archive:
            assert set(archive.namelist()) == {
                "menu.txt",
                "nested/",
                "nested/special.txt",
            }
            assert archive.read("menu.txt") == b"daily menu"
            assert archive.read("nested/special.txt") == b"today's special"

    def test_unzip_dir_extracts_archive_contents(self):
        temp_dir = tempfile.TemporaryDirectory()
        archive_path = os.path.join(temp_dir.name, "menu.zip")
        extract_dir = os.path.join(temp_dir.name, "extracted")

        with zipfile.ZipFile(archive_path, "w") as archive:
            archive.writestr("menu.txt", "daily menu")
            archive.writestr("nested/special.txt", "today's special")

        unzip_dir(archive_path, extract_dir)

        assert open(os.path.join(extract_dir, "menu.txt"), encoding="utf-8").read() == "daily menu"
        assert open(os.path.join(extract_dir, "nested", "special.txt"), encoding="utf-8").read() == "today's special"
