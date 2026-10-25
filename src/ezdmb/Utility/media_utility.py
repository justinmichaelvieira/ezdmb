from pathlib import Path

IMAGE_FILE_EXTENSIONS = (".jpg", ".png", ".gif", ".bmp", ".ico")
TEXT_FILE_EXTENSIONS = (".txt",)
VIDEO_FILE_EXTENSIONS = (
    ".mp4",
    ".m4v",
    ".mov",
    ".avi",
    ".mkv",
    ".webm",
    ".wmv",
    ".mpeg",
    ".mpg",
    ".3gp",
)
CONTENT_FILE_EXTENSIONS = (
    *IMAGE_FILE_EXTENSIONS,
    *TEXT_FILE_EXTENSIONS,
    *VIDEO_FILE_EXTENSIONS,
)
CONTENT_FILE_DIALOG_FILTER = (
    f"Supported content ({' '.join(f'*{extension}' for extension in CONTENT_FILE_EXTENSIONS)});;"
    "All files (*)"
)


def get_content_type(file_name):
    extension = Path(file_name).suffix.casefold()
    if extension in IMAGE_FILE_EXTENSIONS:
        return "image"
    if extension in TEXT_FILE_EXTENSIONS:
        return "text"
    if extension in VIDEO_FILE_EXTENSIONS:
        return "video"
    return None
