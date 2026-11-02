"""Android document-picker access and durable app-private content copies."""

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from PySide6.QtCore import QFile, QFileInfo, QIODevice
from PySide6.QtWidgets import QDialog, QFileDialog

from ezdmb.Utility.media_utility import (
    PRESENTATION_FILE_EXTENSIONS,
    get_content_type,
)
from ezdmb.Utility.path_utility import get_appdata_path


@dataclass(frozen=True)
class picked_document:
    uri: str
    name: str


class document_picker(Protocol):
    def choose_open_documents(
        self, mime_type: str, multiple: bool = False
    ) -> list[picked_document]: ...

    def copy_to_path(self, uri: str, destination: Path) -> None: ...

    def choose_save_document(self, name: str, mime_type: str) -> str | None: ...

    def copy_from_path(self, source: Path, uri: str) -> None: ...


class saf_document_picker:
    """Uses Qt's Android document picker and content-URI file engine."""

    def choose_open_documents(
        self, mime_type: str, multiple: bool = False
    ) -> list[picked_document]:
        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        dialog.setFileMode(
            QFileDialog.FileMode.ExistingFiles
            if multiple
            else QFileDialog.FileMode.ExistingFile
        )
        dialog.setMimeTypeFilters([mime_type])
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return []

        return [
            picked_document(
                url.toString(),
                QFileInfo(url.toString()).fileName(),
            )
            for url in dialog.selectedUrls()
        ]

    def choose_save_document(self, name: str, mime_type: str) -> str | None:
        dialog = QFileDialog()
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setFileMode(QFileDialog.FileMode.AnyFile)
        dialog.setMimeTypeFilters([mime_type])
        dialog.selectFile(name)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return None

        selected_urls = dialog.selectedUrls()
        return selected_urls[0].toString() if selected_urls else None

    def copy_to_path(self, uri: str, destination: Path) -> None:
        source = QFile(uri)
        if not source.open(QIODevice.OpenModeFlag.ReadOnly):
            raise OSError(
                f"Could not read the selected Android document: "
                f"{source.errorString()}"
            )
        try:
            with destination.open("wb") as target:
                while True:
                    chunk = source.read(1024 * 1024).data()
                    if not chunk:
                        if not source.atEnd():
                            raise OSError(
                                f"Could not read the selected Android document: "
                                f"{source.errorString()}"
                            )
                        break
                    if target.write(chunk) != len(chunk):
                        raise OSError(
                            f"Could not copy the selected Android document to "
                            f"{destination}."
                        )
        finally:
            source.close()

    def copy_from_path(self, source: Path, uri: str) -> None:
        destination = QFile(uri)
        if not destination.open(
            QIODevice.OpenModeFlag.WriteOnly
            | QIODevice.OpenModeFlag.Truncate
        ):
            raise OSError(
                f"Could not open the Android destination document: "
                f"{destination.errorString()}"
            )
        try:
            with source.open("rb") as input_file:
                while chunk := input_file.read(1024 * 1024):
                    if destination.write(chunk) != len(chunk):
                        raise OSError(
                            f"Could not write the Android destination document: "
                            f"{destination.errorString()}"
                        )
        finally:
            destination.close()


class android_storage_utility:
    def __init__(
        self,
        app_data_path: str | Path | None = None,
        picker: document_picker | None = None,
    ):
        self._app_data_path = Path(app_data_path or get_appdata_path())
        self._picker = picker
        self._content_directory = self._app_data_path / "content"
        self._staging_directory = self._app_data_path / "staging"

    def pick_content_file(self) -> str | None:
        documents = self._get_picker().choose_open_documents("*/*")
        if not documents:
            return None

        document = documents[0]
        extension = Path(document.name).suffix.casefold()
        if extension in PRESENTATION_FILE_EXTENSIONS:
            raise ValueError(
                "PowerPoint presentations are not supported on Android. "
                "Convert the file to PDF before adding it."
            )
        if get_content_type(document.name) is None:
            raise ValueError(
                "This file type is not supported. Add an image, text file, "
                "video, or PDF."
            )

        destination = self._unique_path(self._content_directory, document.name)
        try:
            self._get_picker().copy_to_path(document.uri, destination)
        except OSError:
            destination.unlink(missing_ok=True)
            raise
        return str(destination)

    def pick_bundle_file(self) -> Path | None:
        documents = self._get_picker().choose_open_documents(
            "application/zip"
        )
        if not documents:
            return None

        document = documents[0]
        if Path(document.name).suffix.casefold() != ".zip":
            raise ValueError("Select a ZIP content bundle.")

        destination = self._unique_path(
            self._staging_directory,
            f"{uuid4().hex}.zip",
        )
        try:
            self._get_picker().copy_to_path(document.uri, destination)
        except OSError:
            destination.unlink(missing_ok=True)
            raise
        return destination

    def release_staged_bundle(self, path: str | Path) -> None:
        staged_path = Path(path).resolve()
        staging_directory = self._staging_directory.resolve()
        if not staged_path.is_relative_to(staging_directory):
            raise ValueError("Refusing to remove a file outside Android staging.")
        staged_path.unlink(missing_ok=True)

    def save_bundle(self, source: str | Path) -> bool:
        source_path = Path(source)
        uri = self._get_picker().choose_save_document(
            source_path.name,
            "application/zip",
        )
        if uri is None:
            return False
        self._get_picker().copy_from_path(source_path, uri)
        return True

    def _get_picker(self) -> document_picker:
        if self._picker is None:
            self._picker = saf_document_picker()
        return self._picker

    @staticmethod
    def _unique_path(directory: Path, name: str) -> Path:
        directory.mkdir(parents=True, exist_ok=True)
        sanitized_name = Path(name.replace("\\", "/")).name.strip(" .")
        if not sanitized_name:
            sanitized_name = "content"

        original = Path(sanitized_name)
        stem = original.stem or "content"
        suffix = original.suffix
        index = 1
        while True:
            candidate_name = (
                sanitized_name
                if index == 1
                else f"{stem} ({index}){suffix}"
            )
            candidate = directory / candidate_name
            try:
                candidate.open("xb").close()
            except FileExistsError:
                index += 1
                continue
            return candidate
