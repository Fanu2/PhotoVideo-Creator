"""
core/models.py

Shared data models.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class SlideshowSettings:
    input_folder: str
    output_video: str

    audio_file: str = ""

    duration: int = 30
    fps: int = 30

    volume: int = 100

    trim_audio: bool = True
    loop_audio: bool = False