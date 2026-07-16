from PySide6.QtCore import Qt

from core.models import SlideshowSettings

from PySide6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSlider,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from worker import VideoWorker


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.worker = None

        self.setWindowTitle("Image Slideshow Creator")
        self.resize(800, 650)

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # -------------------------
        # Input / Output
        # -------------------------

        io_group = QGroupBox("Input / Output")
        io_layout = QGridLayout()

        # Input folder
        io_layout.addWidget(QLabel("Input Folder"), 0, 0)

        self.input_edit = QLineEdit()
        io_layout.addWidget(self.input_edit, 0, 1)

        browse_input = QPushButton("Browse...")
        browse_input.clicked.connect(self.browse_input_folder)
        io_layout.addWidget(browse_input, 0, 2)

        # Output video
        io_layout.addWidget(QLabel("Output Video"), 1, 0)

        self.output_edit = QLineEdit()
        io_layout.addWidget(self.output_edit, 1, 1)

        browse_output = QPushButton("Browse...")
        browse_output.clicked.connect(self.browse_output_file)
        io_layout.addWidget(browse_output, 1, 2)

        io_group.setLayout(io_layout)
        main_layout.addWidget(io_group)

        # Audio Track
        io_layout.addWidget(QLabel("Audio Track"), 2, 0)

        self.audio_edit = QLineEdit()
        io_layout.addWidget(self.audio_edit, 2, 1)

        browse_audio = QPushButton("Browse...")
        browse_audio.clicked.connect(self.browse_audio_file)
        io_layout.addWidget(browse_audio, 2, 2)

        # -------------------------
        # Settings
        # -------------------------

        settings_group = QGroupBox("Video Settings")
        settings_layout = QGridLayout()

        settings_layout.addWidget(QLabel("Duration (seconds)"), 0, 0)

        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1, 86400)
        self.duration_spin.setValue(30)
        settings_layout.addWidget(self.duration_spin, 0, 1)

        settings_layout.addWidget(QLabel("FPS"), 1, 0)

        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(1, 120)
        self.fps_spin.setValue(30)
        settings_layout.addWidget(self.fps_spin, 1, 1)

        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)

        settings_layout.addWidget(QLabel("Volume"), 2, 0)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 200)
        self.volume_slider.setValue(100)

        settings_layout.addWidget(self.volume_slider, 2, 1)

        # -------------------------
        # Progress
        # -------------------------

        self.progress = QProgressBar()
        self.progress.setValue(0)
        main_layout.addWidget(self.progress)

        self.status_label = QLabel("Ready")
        main_layout.addWidget(self.status_label)

        # -------------------------
        # Log
        # -------------------------

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        main_layout.addWidget(self.log)

        # -------------------------
        # Buttons
        # -------------------------

        button_layout = QHBoxLayout()

        self.create_button = QPushButton("Create Video")
        self.create_button.clicked.connect(self.start_video_creation)

        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)

        button_layout.addStretch()
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(exit_button)

        main_layout.addLayout(button_layout)

        self.trim_audio = QCheckBox(
            "Trim audio to video length"
        )

        self.trim_audio.setChecked(True)

        settings_layout.addWidget(
            self.trim_audio,
            3,
            0,
            1,
            2,
        )

        self.loop_audio = QCheckBox(
        
        "Loop audio if shorter"
        )

        settings_layout.addWidget(
            self.loop_audio,
            4,
            0,
            1,
            2,
        )

    # ------------------------------------------------

    def browse_input_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Image Folder"
        )

        if folder:
            self.input_edit.setText(folder)

    def browse_output_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Video",
            "",
            "MP4 Video (*.mp4)"
        )

        if filename:
            if not filename.lower().endswith(".mp4"):
                filename += ".mp4"

            self.output_edit.setText(filename)

    def start_video_creation(self):

        if not self.validate_inputs():
            return

        self.progress.setValue(0)
        self.log.clear()
        self.set_status("Starting...")

        settings = SlideshowSettings(
            input_folder=self.input_edit.text().strip(),
            output_video=self.output_edit.text().strip(),
            audio_file=self.audio_edit.text().strip(),
            duration=self.duration_spin.value(),
            fps=self.fps_spin.value(),
            volume=self.volume_slider.value(),
            trim_audio=self.trim_audio.isChecked(),
            loop_audio=self.loop_audio.isChecked(),
        )

        self.worker = VideoWorker(settings)

        self.worker.progress.connect(self.update_progress)
        self.worker.status.connect(self.set_status)
        self.worker.log.connect(self.log_message)
        self.worker.finished.connect(self.video_finished)
        self.worker.error.connect(self.video_failed)

        self.create_button.setEnabled(False)

        self.worker.start()

    def log_message(self, text):
        self.log.append(text)

    def update_progress(self, value):
        self.progress.setValue(value)

    def set_status(self, text):
        self.status_label.setText(text)

    def video_finished(self):

        self.create_button.setEnabled(True)

        self.progress.setValue(100)

        self.set_status("Completed")

        self.log_message("Video created successfully.")

        QMessageBox.information(
            self,
            "Completed",
            "Video created successfully."
        )

    def video_failed(self, message):

        self.create_button.setEnabled(True)

        self.set_status("Failed")

        QMessageBox.critical(
            self,
            "Error",
            message
        )

    def browse_audio_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Audio File",
            "",
            "Audio Files (*.mp3 *.wav *.aac *.m4a *.flac *.ogg)"
        )

        if filename:
            self.audio_edit.setText(filename)

    def validate_inputs(self):

        if not self.input_edit.text().strip():
            QMessageBox.warning(
                self,
                "Input Folder",
                "Please select an input folder."
            )
            return False

        if not self.output_edit.text().strip():
            QMessageBox.warning(
                self,
                "Output Video",
                "Please select an output video."
            )
            return False

        return True

