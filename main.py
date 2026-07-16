"""
main.py

Application entry point for Image Slideshow Creator.
"""

import sys
import traceback

from PySide6.QtWidgets import QApplication, QMessageBox

from mainwindow import MainWindow


def main() -> int:
    """Start the application."""

    app = QApplication(sys.argv)
    app.setApplicationName("Image Slideshow Creator")
    app.setApplicationVersion("1.0")

    try:
        window = MainWindow()
        window.show()
        return app.exec()

    except Exception:
        traceback.print_exc()

        QMessageBox.critical(
            None,
            "Application Error",
            traceback.format_exc(),
        )

        return 1


if __name__ == "__main__":
    sys.exit(main())