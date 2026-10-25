import pytest

from ezdmb.Utility.media_utility import get_content_type


@pytest.mark.parametrize(
    ("file_name", "expected_type"),
    [
        ("menu.jpg", "image"),
        ("menu.txt", "text"),
        ("menu.mp4", "video"),
        ("menu.MOV", "video"),
        ("menu.webm", "video"),
        ("document.pdf", None),
    ],
)
def test_get_content_type(file_name, expected_type):
    assert get_content_type(file_name) == expected_type
