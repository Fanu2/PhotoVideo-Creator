"""
core/image_utils.py

Image preparation utilities for SlideStudio.
"""

from pathlib import Path
import shutil
import tempfile

from PIL import Image, UnidentifiedImageError
from natsort import natsorted


SUPPORTED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tif",
    ".tiff",
    ".webp",
}


def make_even(value: int) -> int:
    """Return nearest even number."""
    return value if value % 2 == 0 else value - 1


def get_image_files(folder: str):
    """
    Return naturally sorted image files.
    """

    folder = Path(folder)

    if not folder.exists():
        raise FileNotFoundError(
            f"Folder does not exist:\n{folder}"
        )

    files = [
        file
        for file in folder.iterdir()
        if file.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    files = natsorted(files)

    if not files:
        raise RuntimeError(
            "No supported images found."
        )

    return files


def get_target_size(image_files):
    """
    Determine target image size.

    Uses first image.
    Makes dimensions even for H264.
    """

    with Image.open(image_files[0]) as img:

        width, height = img.size

    width = make_even(width)
    height = make_even(height)

    return width, height


def create_working_folder():
    """
    Create temporary working folder.
    """

    return Path(
        tempfile.mkdtemp(prefix="slidestudio_")
    )


def prepare_images(
    image_files,
    progress_callback=None,
    log_callback=None,
):
    """
    Convert images to RGB,
    resize if required,
    save into temporary folder.

    Returns

    working_folder

    processed_images

    target_size
    """

    width, height = get_target_size(image_files)

    if log_callback:
        log_callback(
            f"Target size : {width} x {height}"
        )

    work = create_working_folder()

    processed = []

    total = len(image_files)

    for index, image in enumerate(
        image_files,
        start=1,
    ):

        try:

            with Image.open(image) as img:

                img = img.convert("RGB")

                if img.size != (width, height):

                    img = img.resize(
                        (width, height),
                        Image.LANCZOS,
                    )

                outfile = (
                    work /
                    f"{index:06d}.jpg"
                )

                img.save(
                    outfile,
                    quality=95,
                    optimize=True,
                )

                processed.append(outfile)

        except UnidentifiedImageError as e:

            raise RuntimeError(
                f"Invalid image:\n{image}"
            ) from e

        if progress_callback:

            progress_callback(
                int(index / total * 50)
            )

    return work, processed, (width, height)


def cleanup(working_folder):
    """
    Remove temporary files.
    """

    shutil.rmtree(
        working_folder,
        ignore_errors=True,
    )