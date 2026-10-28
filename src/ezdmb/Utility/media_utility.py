import shutil
import subprocess
import tempfile
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
PDF_FILE_EXTENSIONS = (".pdf",)
PRESENTATION_FILE_EXTENSIONS = (".ppt", ".pptx")
CONTENT_FILE_EXTENSIONS = (
    *IMAGE_FILE_EXTENSIONS,
    *TEXT_FILE_EXTENSIONS,
    *VIDEO_FILE_EXTENSIONS,
    *PDF_FILE_EXTENSIONS,
    *PRESENTATION_FILE_EXTENSIONS,
)
CONTENT_FILE_DIALOG_FILTER = (
    f"Supported content ({' '.join(f'*{extension}' for extension in CONTENT_FILE_EXTENSIONS)});;"
    "All files (*)"
)


def is_web_url(value):
    return str(value).strip().casefold().startswith(("http://", "https://"))


def convert_presentation_to_pdf(presentation_path):
    """Convert a presentation to PDF with LibreOffice; returns the PDF path."""
    source = Path(presentation_path).resolve()
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice is None:
        for candidate in (
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
        ):
            if Path(candidate).exists():
                soffice = candidate
                break
    if soffice is None:
        raise RuntimeError("LibreOffice is required to display presentations.")

    stamp = f"{source.stat().st_mtime_ns}"
    output_dir = Path(tempfile.gettempdir()) / "ezdmb_presentations" / stamp
    output_pdf = output_dir / f"{source.stem}.pdf"
    if output_pdf.exists():
        return str(output_pdf)

    output_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            soffice,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(output_dir),
            str(source),
        ],
        check=True,
        capture_output=True,
        timeout=180,
    )
    if not output_pdf.exists():
        raise RuntimeError(f"Presentation conversion failed: {source}")
    return str(output_pdf)


def get_content_type(file_name):
    if is_web_url(file_name):
        return "web"
    extension = Path(file_name).suffix.casefold()
    if extension in IMAGE_FILE_EXTENSIONS:
        return "image"
    if extension in TEXT_FILE_EXTENSIONS:
        return "text"
    if extension in VIDEO_FILE_EXTENSIONS:
        return "video"
    if extension in PDF_FILE_EXTENSIONS:
        return "pdf"
    if extension in PRESENTATION_FILE_EXTENSIONS:
        return "presentation"
    return None
