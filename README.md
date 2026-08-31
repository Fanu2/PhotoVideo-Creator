Here is a **complete, directly pasteable `README.md`** based on that code:

````markdown
# 🎬 Image Slideshow Video Maker

A Python utility for converting a folder of images into a high-quality MP4 slideshow video.

The application scans a folder for supported images, sorts them naturally, processes them into a consistent format and size, and creates an H.264 MP4 video using MoviePy and FFmpeg.

---

## ✨ Features

- 🖼️ Convert a folder of images into a video
- 🎬 Create high-quality MP4 slideshow videos
- 🔢 Natural filename sorting
- 📁 Automatic image folder scanning
- 🖼️ Support for multiple image formats
- 📐 Automatic image resizing
- ⚖️ Consistent video frame dimensions
- 🔢 Automatic even-number dimension correction
- 🎞️ Configurable video duration
- 🎥 Configurable frames per second (FPS)
- 📊 Progress callback support
- 📢 Status callback support
- 📝 Logging callback support
- 🧹 Automatic temporary file cleanup
- 🛡️ Basic corrupt-image detection
- 📦 H.264 video encoding
- 🎨 Compatible `yuv420p` pixel format

---

## 🖼️ Supported Image Formats

The application supports:

- PNG
- JPG
- JPEG
- BMP
- TIF
- TIFF
- WEBP

Example:

```text
images/
├── image1.jpg
├── image2.jpg
├── image3.png
├── image10.jpg
└── image11.webp
```

Files are naturally sorted, ensuring that filenames such as:

```text
image1.jpg
image2.jpg
image10.jpg
```

are placed in the expected order.

---

## 📁 How It Works

The video creation process follows these steps:

1. Scan the selected image folder.
2. Find supported image files.
3. Sort images naturally.
4. Read the dimensions of the first image.
5. Calculate a valid target size.
6. Convert images to RGB.
7. Resize images when necessary.
8. Save processed images temporarily.
9. Calculate the display duration for each image.
10. Create an image sequence.
11. Encode the video as H.264 MP4.
12. Clean up temporary files automatically.

---

## 📐 Image Processing

Video encoders commonly require even-numbered frame dimensions.

The application automatically adjusts image dimensions when required.

For example:

```text
1921 × 1081
```

becomes:

```text
1920 × 1080
```

This helps ensure compatibility with the H.264 encoder.

---

## 🎞️ Video Settings

The generated video uses:

```text
Codec: libx264
Pixel Format: yuv420p
Audio: Disabled
Preset: medium
CRF: 18
```

These settings provide high-quality output with good compatibility across video players and devices.

---

## 🚀 Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-folder>
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## 📦 Requirements

The project uses the following Python packages:

```text
moviepy
Pillow
natsort
```

Example `requirements.txt`:

```text
moviepy
Pillow
natsort
```

MoviePy requires FFmpeg for video encoding.

---

## 🖥️ Example Usage

The main function can be used like this:

```python
from slideshow_video import create_video

create_video(
    input_folder="images",
    output_video="output/video.mp4",
    duration=60,
    fps=30,
)
```

This creates a 60-second slideshow video at 30 FPS.

---

## 📊 Progress Support

The application supports optional callbacks for integrating with GUI applications.

Example:

```python
def show_progress(value):
    print(f"Progress: {value}%")
```

Pass the callback:

```python
create_video(
    input_folder="images",
    output_video="output.mp4",
    duration=60,
    fps=30,
    progress_callback=show_progress,
)
```

---

## 📢 Status Support

A status callback can be used to display the current operation:

```python
def show_status(message):
    print(message)
```

Example:

```python
create_video(
    input_folder="images",
    output_video="output.mp4",
    duration=60,
    fps=30,
    status_callback=show_status,
)
```

Possible status messages include:

```text
Scanning folder...
Preparing images...
Encoding video...
Completed
```

---

## 📝 Logging Support

The application also supports logging callbacks.

Example:

```python
def log_message(message):
    print(message)
```

Logs may include:

```text
Found 25 image(s).
Original Size : 1920 x 1080
Target Size   : 1920 x 1080
Video created successfully.
```

---

## 🛡️ Error Handling

The application checks for common problems, including:

- Input folder does not exist
- No supported image files found
- Invalid duration
- Invalid FPS value
- Corrupt or unsupported image files

Examples of possible errors:

```text
No supported image files found.
```

```text
Duration must be greater than zero.
```

```text
FPS must be greater than zero.
```

---

## 🧹 Temporary File Management

Images are processed inside a temporary directory.

The temporary files are automatically removed after video creation, including when an error occurs.

This prevents unnecessary processed-image files from remaining on the system.

---

## 📁 Suggested Project Structure

```text
image-slideshow-video-maker/
├── slideshow_video.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── images/
```

---

## 🚧 Future Improvements

Possible future features include:

- 🎵 Background music
- 🎙️ Voice narration
- ✨ Fade transitions
- 🎬 Custom transitions
- 📝 Text overlays
- 🖼️ Image captions
- 🎨 Aspect ratio selection
- 📱 Vertical video support
- ▶️ Video preview
- 🖥️ Desktop GUI
- 📂 Drag-and-drop folders
- ⏸️ Pause and cancel rendering
- 🎥 Multiple output resolutions
- 🔊 Audio mixing

---

## 👤 Author

Jasvir Singh Sidhu

GitHub: Fanu2

---

## 📄 License

This project is intended for personal, educational, and experimental use.

---

# 🎬 Image Slideshow Video Maker

*Turn your images into a story.*
````
