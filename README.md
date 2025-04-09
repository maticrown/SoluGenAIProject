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

#bash
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

---

## ✅ Stage 3 – Graceful Termination

This stage ensures that all processes (streamer, detector, and display) exit cleanly once the video ends.

### ✔️ Key Behavior:
- When the video stream ends, the **streamer sends a sentinel value `"END"`**.
- The **detector receives "END"**, forwards it to the display, and stops.
- The **display** exits when it receives `"END"`, or immediately if the user presses `q`.

### 🔄 Why it matters:
Without graceful shutdown, some processes may remain hanging in memory, waiting forever for new data.  
This design guarantees a complete and clean pipeline teardown with no orphaned processes.

### 💬 Notes:
- The streamer may finish first, but the other processes will continue until they have processed all queued frames.
- The short delay between streamer exit and full shutdown is intentional and ensures no data is lost.

---

## 📅 Status

✅ Stage 1 – Motion detection  
✅ Stage 2 – Blurring motion regions  
✅ Stage 3 – Graceful termination and process shutdown  

## 🚦 Pipeline Overview

| Stage  | Description                         | Status |
|--------|-------------------------------------|--------|
| 1      | Motion detection with bounding boxes | ✅ Done |
| 2      | Blurring of detected regions        | ✅ Done |
| 3      | Clean shutdown of all processes     | ✅ Done |