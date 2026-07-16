"""
core/audio_utils.py

Audio utility functions for SlideStudio.
"""

from pathlib import Path

from moviepy import AudioFileClip
from moviepy.audio.fx.AudioLoop import AudioLoop
from moviepy.audio.fx.MultiplyVolume import MultiplyVolume


SUPPORTED_AUDIO = {
    ".mp3",
    ".wav",
    ".aac",
    ".m4a",
    ".flac",
    ".ogg",
}


def load_audio(audio_file: str):
    """
    Load an audio file.

    Returns
    -------
    AudioFileClip or None
    """

    if not audio_file:
        return None

    audio_path = Path(audio_file)

    if not audio_path.exists():
        raise FileNotFoundError(
            f"Audio file not found:\n{audio_file}"
        )

    if audio_path.suffix.lower() not in SUPPORTED_AUDIO:
        raise RuntimeError(
            f"Unsupported audio format:\n{audio_path.suffix}"
        )

    return AudioFileClip(str(audio_path))


def prepare_audio(
    audio_clip,
    video_duration: float,
    volume: int = 100,
    trim_audio: bool = True,
    loop_audio: bool = False,
):
    """
    Prepare an audio clip for the slideshow.

    Returns
    -------
    AudioClip or None
    """

    if audio_clip is None:
        return None

    # Trim if longer
    if trim_audio and audio_clip.duration > video_duration:
        audio_clip = audio_clip.subclipped(
            0,
            video_duration,
        )

    # Loop if shorter
    if loop_audio and audio_clip.duration < video_duration:
        audio_clip = audio_clip.with_effects(
            [
                AudioLoop(duration=video_duration)
            ]
        )

    # Apply volume
    volume_scale = volume / 100.0

    audio_clip = audio_clip.with_effects(
        [
            MultiplyVolume(volume_scale)
        ]
    )

    return audio_clip