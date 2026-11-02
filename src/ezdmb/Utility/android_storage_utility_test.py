from pathlib import Path
from types import SimpleNamespace

import pytest
from PySide6.QtCore import QByteArray, QIODevice, QUrl
from PySide6.QtWidgets import QDialog, QFileDialog

import ezdmb.Utility.android_storage_utility as storage_utility_module
from ezdmb.Controller.configuration import (
    configuration,
    default_time_blocks,
)
from ezdmb.Utility.android_storage_utility import (
    android_storage_utility,
    picked_document,
    saf_document_picker,
)


class fake_document_picker:
    def __init__(self):
        self.documents = []
        self.contents = {}
        self.saved_documents = {}
        self.selected_destination = "content://documents/export"

    def choose_open_documents(self, mime_type, multiple=False):
        return self.documents

    def copy_to_path(self, uri, destination):
        destination.write_bytes(self.contents[uri])

    def choose_save_document(self, name, mime_type):
        return self.selected_destination

    def copy_from_path(self, source, uri):
        self.saved_documents[uri] = source.read_bytes()


class TestAndroidStorageUtility:
    def test_copies_selected_content_to_persistent_private_storage(self, tmp_path):
        picker = fake_document_picker()
        picker.documents = [picked_document("content://menu/1", "menu.png")]
        picker.contents["content://menu/1"] = b"menu image"
        adapter = android_storage_utility(tmp_path, picker)

        selected_content_path = adapter.pick_content_file()
        assert selected_content_path is not None
        selected_path = Path(selected_content_path)
        restarted_adapter = android_storage_utility(tmp_path, picker)

        assert selected_path == tmp_path / "content" / "menu.png"
        assert selected_path.read_bytes() == b"menu image"
        assert restarted_adapter._content_directory == tmp_path / "content"

    def test_selected_private_path_survives_configuration_reload(
        self,
        tmp_path,
        monkeypatch,
    ):
        monkeypatch.setattr(
            "ezdmb.Controller.configuration.get_appdata_path",
            lambda: str(tmp_path),
        )
        picker = fake_document_picker()
        picker.documents = [picked_document("content://menu/1", "menu.txt")]
        picker.contents["content://menu/1"] = b"daily menu"
        adapter = android_storage_utility(tmp_path, picker)
        content_path = adapter.pick_content_file()
        assert content_path is not None
        config = configuration()
        content_groups = [
            {
                "id": "default",
                "name": "Default",
                "content": [content_path],
            }
        ]

        config.save_config(
            True,
            15,
            [content_path],
            TimeBlocks=default_time_blocks(),
            ContentGroups=content_groups,
            RotationMode="interval",
        )
        reloaded_config = configuration()

        assert reloaded_config.ContentArray == [content_path]
        assert Path(content_path).read_bytes() == b"daily menu"

    def test_duplicate_filenames_receive_distinct_app_owned_paths(self, tmp_path):
        picker = fake_document_picker()
        picker.documents = [picked_document("content://menu/1", "menu.txt")]
        picker.contents["content://menu/1"] = b"first"
        adapter = android_storage_utility(tmp_path, picker)

        first_content_path = adapter.pick_content_file()
        assert first_content_path is not None
        first_path = Path(first_content_path)
        picker.contents["content://menu/1"] = b"second"
        second_content_path = adapter.pick_content_file()
        assert second_content_path is not None
        second_path = Path(second_content_path)

        assert first_path != second_path
        assert first_path.read_bytes() == b"first"
        assert second_path.read_bytes() == b"second"

    def test_rejects_presentations_before_copying_them(self, tmp_path):
        picker = fake_document_picker()
        picker.documents = [picked_document("content://slides/1", "slides.pptx")]
        adapter = android_storage_utility(tmp_path, picker)

        with pytest.raises(ValueError, match="not supported on Android"):
            adapter.pick_content_file()

        assert not (tmp_path / "content").exists()

    def test_bundle_import_stages_in_private_storage_and_releases_stage(
        self, tmp_path
    ):
        picker = fake_document_picker()
        picker.documents = [picked_document("content://bundles/1", "menu.zip")]
        picker.contents["content://bundles/1"] = b"zip contents"
        adapter = android_storage_utility(tmp_path, picker)

        staged_path = adapter.pick_bundle_file()

        assert staged_path is not None
        assert staged_path.parent == tmp_path / "staging"
        assert staged_path.read_bytes() == b"zip contents"
        adapter.release_staged_bundle(staged_path)
        assert not staged_path.exists()

    def test_refuses_to_release_a_file_outside_the_staging_directory(self, tmp_path):
        adapter = android_storage_utility(tmp_path, fake_document_picker())
        external_path = tmp_path / "user-file.zip"
        external_path.write_bytes(b"keep")

        with pytest.raises(ValueError, match="outside Android staging"):
            adapter.release_staged_bundle(external_path)

        assert external_path.read_bytes() == b"keep"

    def test_saves_bundle_to_user_selected_document(self, tmp_path):
        picker = fake_document_picker()
        adapter = android_storage_utility(tmp_path, picker)
        bundle_path = tmp_path / "ezdmb_bundle.zip"
        bundle_path.write_bytes(b"zip contents")

        assert adapter.save_bundle(bundle_path)
        assert picker.saved_documents[picker.selected_destination] == b"zip contents"

    def test_saf_picker_uses_qt_dialog_and_preserves_content_uri(
        self,
        monkeypatch,
    ):
        class fake_file_dialog:
            AcceptMode = QFileDialog.AcceptMode
            FileMode = QFileDialog.FileMode

            def __init__(self):
                self.selected_urls = [
                    QUrl("content://documents/menu/1"),
                    QUrl("content://documents/menu/2"),
                ]
                self.result = QDialog.DialogCode.Accepted

            def setAcceptMode(self, accept_mode):
                self.accept_mode = accept_mode

            def setFileMode(self, file_mode):
                self.file_mode = file_mode

            def setMimeTypeFilters(self, mime_types):
                self.mime_types = mime_types

            def exec(self):
                return self.result

            def selectedUrls(self):
                return self.selected_urls

        dialog = fake_file_dialog()

        class fake_file_dialog_factory:
            AcceptMode = QFileDialog.AcceptMode
            FileMode = QFileDialog.FileMode

            def __call__(self):
                return dialog

        monkeypatch.setattr(
            storage_utility_module,
            "QFileDialog",
            fake_file_dialog_factory(),
        )
        monkeypatch.setattr(
            storage_utility_module,
            "QFileInfo",
            lambda _uri: SimpleNamespace(fileName=lambda: "menu.png"),
        )

        documents = saf_document_picker().choose_open_documents(
            "image/*",
            multiple=True,
        )

        assert dialog.accept_mode == (
            QFileDialog.AcceptMode.AcceptOpen
        )
        assert dialog.file_mode == (
            QFileDialog.FileMode.ExistingFiles
        )
        assert dialog.mime_types == ["image/*"]
        assert documents == [
            picked_document("content://documents/menu/1", "menu.png"),
            picked_document("content://documents/menu/2", "menu.png"),
        ]

    def test_saf_picker_copies_content_uri_streams(self, tmp_path, monkeypatch):
        content = b"menu content" * 100_000
        documents = {"content://documents/menu/1": content}

        class fake_qfile:
            def __init__(self, uri):
                self.uri = uri
                self.position = 0
                self.output = bytearray()
                self.documents = documents

            def open(self, mode):
                if mode & QIODevice.OpenModeFlag.ReadOnly:
                    return self.uri in self.documents
                return True

            def read(self, size):
                chunk = self.documents[self.uri][self.position : self.position + size]
                self.position += len(chunk)
                return QByteArray(chunk)

            def atEnd(self):
                return self.position >= len(self.documents[self.uri])

            def write(self, data):
                self.output.extend(data)
                self.documents[self.uri] = bytes(self.output)
                return len(data)

            def errorString(self):
                return "mock Qt file error"

            def close(self):
                pass

        monkeypatch.setattr(storage_utility_module, "QFile", fake_qfile)
        picker = saf_document_picker()
        imported = tmp_path / "menu.png"
        picker.copy_to_path("content://documents/menu/1", imported)

        exported = tmp_path / "export.zip"
        exported.write_bytes(b"bundle content")
        picker.copy_from_path(exported, "content://documents/menu/export.zip")

        assert imported.read_bytes() == content
        assert (
            documents["content://documents/menu/export.zip"]
            == b"bundle content"
        )
