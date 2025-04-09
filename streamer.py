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
    start_time = time.time()

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

    # third step change
    # Send termination signal to downstream process
    output_queue.put("END")

    print("[Streamer] Sent END signal to detector.")

    # Calculate and print total run time
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"[Streamer] Sent END signal to detector.")
    print(f"[Streamer] Stream ended after {frame_id} frames, {elapsed:.2f} seconds.")

    # Note:
    # Although the streamer finishes immediately after sending "END",
    # the detector and display processes may still be processing frames
    # already in the queue. This is expected behavior, as each stage
    # completes all frames before shutting down.
