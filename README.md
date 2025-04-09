# SoluGenAIProject

This repository contains my solution for the home assignment given by **SoluGenAI**  
for the position of **Senior Python Developer**.

---

## ✅ Stage 1 – Motion Detection Pipeline

This stage implements the basic video processing pipeline, consisting of three independent processes:

1. **Streamer** – Reads frames from a video URL using OpenCV and pushes them to a queue.
2. **Detector** – Detects motion using frame differencing and forwards detection boxes.
3. **Display** – Displays the frames with bounding boxes around motion regions and a timestamp.

### Technologies Used:
- Python 3.8
- OpenCV
- Multiprocessing (Queue & Process)

---

├── main.py # Entry point: sets up the processes 
├── streamer.py # Video reader (supports URL input) 
├── detector.py # Motion detection logic 
├── display.py # Visualization with timestamp 
├── README.md # This file
└── .gitignore # Excludes cache/video files

---

## ▶️ How to Run
# Note: enter the link to the video required for input, below is an example 

```bash
python main.py "https://github.com/opencv/opencv/raw/master/samples/data/vtest.avi"

---

## ✅ Stage 2 – Blurring Detected Motion

In this stage, motion detection is enhanced by applying **Gaussian blur**  
to all detected regions before displaying the frame.

### ✔️ Key Updates:
- **Blurring is done only inside the `display.py` component**, as required.
- The system continues to show a live timestamp and support real-time streaming.

### 📌 Technical Notes:
- **Gaussian blur** was selected for its smooth and natural effect, suitable for masking motion.
- Blurring kernel size is `(51, 51)`, which can be adjusted for performance or effect.
- The blurring is applied only to bounding boxes (`ROI`) received from the detector.

### 🎥 Visual Effect:
Each object in motion appears blurred in the display window, while the rest of the frame remains sharp.

---

⬜ Stage 3 – Graceful shutdown of all processes
