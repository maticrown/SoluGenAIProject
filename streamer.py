# OpenCV for handling video capture
import cv2
import time


def stream_video(video_path, output_queue):
    """
    Reads frames from a video file and puts them into a queue.
    :param video_path: Path to the video file
    :param output_queue: Queue to send frames to the detector
    """
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if file successfully opens
    if not cap.isOpened():
        print(f"Failed to open video stream: {video_path}")
        return

    frame_id = 0
    while cap.isOpened():
        # Read one frame at a time
        ret, frame = cap.read()
        # No more frames to read
        if not ret:
            print("[Streamer] End of video stream.")
            break  # End of video

        frame_id += 1
        # Send the frame to the next component (detector)
        output_queue.put(frame)
        time.sleep(0.03)  # 30 FPS ~ 33ms delay for better quality

    # Release video file resources
    cap.release()
    # Note: In the third level of the project we will notify the next process
    # that the video has ended
