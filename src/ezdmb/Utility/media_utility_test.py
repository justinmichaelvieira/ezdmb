from unittest.mock import patch

import pytest

from ezdmb.Utility.media_utility import (
    convert_presentation_to_pdf,
    get_content_type,
)


@pytest.mark.parametrize(
    ("file_name", "expected_type"),
    [
        ("menu.jpg", "image"),
        ("menu.txt", "text"),
        ("menu.mp4", "video"),
        ("menu.MOV", "video"),
        ("menu.webm", "video"),
        ("document.pdf", "pdf"),
        ("slides.PPT", "presentation"),
        ("slides.pptx", "presentation"),
        ("https://example.com/menu", "web"),
        ("document.docx", None),
    ],
)
def test_get_content_type(file_name, expected_type):
    assert get_content_type(file_name) == expected_type


def test_presentation_conversion_is_disabled_on_android(tmp_path):
    presentation_path = tmp_path / "slides.pptx"
    presentation_path.write_bytes(b"presentation")

    with (
        patch("ezdmb.Utility.media_utility.is_android", return_value=True),
        pytest.raises(RuntimeError, match="not supported on Android"),
    ):
        convert_presentation_to_pdf(presentation_path)
