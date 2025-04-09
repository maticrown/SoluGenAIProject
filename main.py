# Handles command-line arguments parsing
import argparse
# Used to run each system component in its own process
# and communicate via Queues
from multiprocessing import Process, Queue
# Imports the main functions of each component
from streamer import stream_video
from detector import detect_motion
from display import display_frames


def main(video_path):
    """
    Initializes and runs the three system components:
    Streamer, Detector, and Display.
    :param video_path: Path to the input video file
    """

    print("[Main] Initializing queues and processes...")

    # Create inter-process communication queues
    stream_to_detect = Queue()
    detect_to_display = Queue()

    # Set up each component as a separate process
    streamer = Process(target=stream_video, args=(video_path, stream_to_detect))
    detector = Process(target=detect_motion, args=(stream_to_detect, detect_to_display))
    displayer = Process(target=display_frames, args=(detect_to_display,))

    print("[Main] Starting all processes")
    # Start all processes
    streamer.start()
    detector.start()
    displayer.start()

    print("[Main] Waiting for processes to finish")
    # Wait for all processes to complete
    streamer.join()
    detector.join()
    displayer.join()


if __name__ == "__main__":
    # Parse video path from command line arguments
    parser = argparse.ArgumentParser(description="Video Analytics System - Motion Detection")
    parser.add_argument("video_path", help="Path to the input video file")
    args = parser.parse_args()

    # Run the main function with the provided video path
    main(args.video_path)

    print("[Main] All processes finished.")
