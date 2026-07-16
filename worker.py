"""
worker.py

Background worker thread for slideshow creation.
"""

from PySide6.QtCore import QThread, Signal

from core.models import SlideshowSettings
from core.video_creator import create_video


class VideoWorker(QThread):
    """Background worker for slideshow creation."""

    progress = Signal(int)
    status = Signal(str)
    log = Signal(str)

    finished = Signal()
    error = Signal(str)

    def __init__(self, settings: SlideshowSettings):
        super().__init__()

        self.settings = settings

    def run(self):
        """Run slideshow creation in a background thread."""

        try:

            create_video(
                settings=self.settings,
                progress_callback=self.progress.emit,
                status_callback=self.status.emit,
                log_callback=self.log.emit,
            )

            self.finished.emit()

        except Exception as exc:

            self.error.emit(str(exc))