import zipfile

from ezdmb.Utility.bundle_utility import unzip_dir, zip_dir


class bundle_utility_test:
    def test_zip_dir_preserves_files_and_relative_paths(self, tmp_path):
        source_dir = tmp_path / "source"
        nested_dir = source_dir / "nested"
        nested_dir.mkdir(parents=True)
        (source_dir / "menu.txt").write_text("daily menu", encoding="utf-8")
        (nested_dir / "special.txt").write_text("today's special", encoding="utf-8")
        archive_path = tmp_path / "menu.zip"

        zip_dir(source_dir, archive_path)

        with zipfile.ZipFile(archive_path) as archive:
            assert set(archive.namelist()) == {
                "menu.txt",
                "nested/",
                "nested/special.txt",
            }
            assert archive.read("menu.txt") == b"daily menu"
            assert archive.read("nested/special.txt") == b"today's special"

    def test_unzip_dir_extracts_archive_contents(self, tmp_path):
        archive_path = tmp_path / "menu.zip"
        extract_dir = tmp_path / "extracted"

        with zipfile.ZipFile(archive_path, "w") as archive:
            archive.writestr("menu.txt", "daily menu")
            archive.writestr("nested/special.txt", "today's special")

        unzip_dir(archive_path, extract_dir)

        assert (extract_dir / "menu.txt").read_text(encoding="utf-8") == "daily menu"
        assert (
            extract_dir / "nested" / "special.txt"
        ).read_text(encoding="utf-8") == "today's special"
