"""
core/video_creator.py

Main slideshow creation engine.
"""

from pathlib import Path

from moviepy import ImageSequenceClip

from .audio_utils import load_audio, prepare_audio
from .image_utils import (
    cleanup,
    get_image_files,
    prepare_images,
)
from .models import SlideshowSettings


def create_video(
    settings: SlideshowSettings,
    progress_callback=None,
    status_callback=None,
    log_callback=None,
):
    """
    Create a slideshow video.
    """

    if settings.duration <= 0:
        raise ValueError("Duration must be greater than zero.")

    if settings.fps <= 0:
        raise ValueError("FPS must be greater than zero.")

    if status_callback:
        status_callback("Scanning images...")

    image_files = get_image_files(settings.input_folder)

    if log_callback:
        log_callback(f"Found {len(image_files)} image(s).")

    working_folder, processed_images, target_size = prepare_images(
        image_files=image_files,
        progress_callback=progress_callback,
        log_callback=log_callback,
    )

    try:

        if status_callback:
            status_callback("Creating slideshow...")

        seconds_per_image = (
            settings.duration / len(processed_images)
        )

        clip = ImageSequenceClip(
            [str(image) for image in processed_images],
            durations=[seconds_per_image] * len(processed_images),
        )

        # --------------------------------------------------
        # Audio
        # --------------------------------------------------

        if settings.audio_file:

            if status_callback:
                status_callback("Preparing audio...")

            if log_callback:
                log_callback(
                    f"Audio : {Path(settings.audio_file).name}"
                )

            audio = load_audio(settings.audio_file)

            audio = prepare_audio(
                audio_clip=audio,
                video_duration=clip.duration,
                volume=settings.volume,
                trim_audio=settings.trim_audio,
                loop_audio=settings.loop_audio,
            )

            if audio is not None:
                clip = clip.with_audio(audio)

        # --------------------------------------------------
        # Output
        # --------------------------------------------------

        if status_callback:
            status_callback("Encoding video...")

        output_path = Path(settings.output_video)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        clip.write_videofile(
            str(output_path),
            fps=settings.fps,
            codec="libx264",
            preset="medium",
            audio=bool(settings.audio_file),
            ffmpeg_params=[
                "-pix_fmt",
                "yuv420p",
                "-crf",
                "18",
            ],
        )

        clip.close()

        if progress_callback:
            progress_callback(100)

        if status_callback:
            status_callback("Completed")

        if log_callback:
            log_callback("Video created successfully.")

    finally:

        cleanup(working_folder)