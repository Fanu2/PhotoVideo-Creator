import shutil
import tempfile
from pathlib import Path

from moviepy.editor import ImageSequenceClip
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


def log(callback, message):
    if callback:
        callback(message)


def status(callback, message):
    if callback:
        callback(message)


def progress(callback, value):
    if callback:
        callback(value)


def even(value):
    """Return nearest even integer."""
    return value if value % 2 == 0 else value - 1


def get_image_files(folder):

    folder = Path(folder)

    if not folder.exists():
        raise FileNotFoundError(folder)

    files = [
        f
        for f in folder.iterdir()
        if f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    files = natsorted(files)

    if not files:
        raise RuntimeError("No supported image files found.")

    return files


def create_video(
    input_folder,
    output_video,
    duration,
    fps,
    progress_callback=None,
    status_callback=None,
    log_callback=None,
):

    if duration <= 0:
        raise ValueError("Duration must be greater than zero.")

    if fps <= 0:
        raise ValueError("FPS must be greater than zero.")

    status(status_callback, "Scanning folder...")

    image_files = get_image_files(input_folder)

    log(log_callback, f"Found {len(image_files)} image(s).")

    output_video = Path(output_video)

    output_video.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(image_files[0]) as img:

        original_size = img.size

    target_size = (
        even(original_size[0]),
        even(original_size[1]),
    )

    log(
        log_callback,
        f"Original Size : {original_size[0]} x {original_size[1]}"
    )

    log(
        log_callback,
        f"Target Size   : {target_size[0]} x {target_size[1]}"
    )

    temp_dir = Path(tempfile.mkdtemp(prefix="slideshow_"))

    processed_files = []

    try:

        total = len(image_files)

        status(status_callback, "Preparing images...")

        for index, image_path in enumerate(image_files, start=1):

            try:

                with Image.open(image_path) as img:

                    img = img.convert("RGB")

                    if img.size != target_size:
                        img = img.resize(
                            target_size,
                            Image.LANCZOS
                        )

                    outfile = temp_dir / f"{index:06d}.jpg"

                    img.save(
                        outfile,
                        quality=95,
                        optimize=True,
                    )

                    processed_files.append(str(outfile))

            except UnidentifiedImageError:
                raise RuntimeError(
                    f"Unsupported or corrupt image:\n{image_path}"
                )

            progress(
                progress_callback,
                int(index * 50 / total),
            )

        status(status_callback, "Encoding video...")

        seconds_per_image = duration / len(processed_files)

        clip = ImageSequenceClip(
            processed_files,
            durations=[seconds_per_image] * len(processed_files),
        )

        clip.write_videofile(
            str(output_video),
            fps=fps,
            codec="libx264",
            audio=False,
            preset="medium",
            ffmpeg_params=[
                "-pix_fmt",
                "yuv420p",
                "-crf",
                "18",
            ],
        )

        clip.close()

        progress(progress_callback, 100)

        status(status_callback, "Completed")

        log(log_callback, "Video created successfully.")

    finally:

        shutil.rmtree(temp_dir, ignore_errors=True)