import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import Mock, patch

from ezdmb.Utility.bundle_utility import (
    export_bundle,
    import_bundle,
    unzip_dir,
    zip_dir,
)


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

        with open(os.path.join(extract_dir, "menu.txt"), encoding="utf-8") as f:
            assert f.read() == "daily menu"
        with open(os.path.join(extract_dir, "nested", "special.txt"), encoding="utf-8") as f:
            assert f.read() == "today's special"

    def test_import_bundle_extracts_files_and_updates_configuration(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            archive_path = root / "bundle.zip"
            appdata_path = root / "appdata"
            extract_path = appdata_path / "ezdmb_bundle"
            extract_path.mkdir(parents=True)
            (extract_path / "stale.txt").write_text("stale", encoding="utf-8")
            with zipfile.ZipFile(archive_path, "w") as archive:
                archive.writestr("dmb_config.json", '{"rotate": true}')
                archive.writestr("menu.png", "image data")

            config = Mock()
            with (
                patch(
                    "ezdmb.Utility.bundle_utility.QFileDialog.getOpenFileName",
                    return_value=(str(archive_path), ""),
                ),
                patch(
                    "ezdmb.Utility.bundle_utility.get_appdata_path",
                    return_value=appdata_path,
                ),
            ):
                import_bundle(config, True)

            assert config.ConfigPath == os.path.join(extract_path, "dmb_config.json")
            assert not (extract_path / "stale.txt").exists()
            assert (extract_path / "menu.png").read_text(encoding="utf-8") == "image data"

    def test_import_bundle_does_not_change_configuration_when_cancelled(self):
        config = Mock()
        config.ConfigPath = Path("current-config.json")
        config.ContentArray = [Path("current-menu.png")]

        with (
            patch(
                "ezdmb.Utility.bundle_utility.QFileDialog.getOpenFileName",
                return_value=("", ""),
            ),
            patch("ezdmb.Utility.bundle_utility.get_appdata_path") as get_appdata_path,
        ):
            import_bundle(config, True)

        assert config.ConfigPath == Path("current-config.json")
        assert config.ContentArray == [Path("current-menu.png")]
        get_appdata_path.assert_not_called()

    def test_export_bundle_creates_zip_with_configuration_and_content(self):
        previous_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            config_path = root / "config.json"
            content_path = root / "menu.png"
            output_path = root / "output"
            staging_path = root / "staging"
            output_path.mkdir()
            staging_path.mkdir()
            config_path.write_text('{"rotate": true}', encoding="utf-8")
            content_path.write_text("image data", encoding="utf-8")
            config = Mock()
            config.ConfigPath = config_path
            config.ContentArray = [content_path]

            try:
                os.chdir(root)
                with (
                    patch(
                        "ezdmb.Utility.bundle_utility.QFileDialog.getExistingDirectory",
                        return_value=str(output_path),
                    ),
                ):
                    export_bundle(config, True)

                bundle_path = output_path / "ezdmb_bundle.zip"
                with zipfile.ZipFile(bundle_path) as archive:
                    assert set(archive.namelist()) == {"dmb_config.json", "menu.png"}
                    assert archive.read("dmb_config.json") == b'{"rotate": true}'
                    assert archive.read("menu.png") == b"image data"
            finally:
                os.chdir(previous_cwd)
