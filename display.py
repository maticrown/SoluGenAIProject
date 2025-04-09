import cv2
from datetime import datetime


def display_frames(input_queue):
    """
    Displays video frames with motion detection rectangles and a timestamp overlay.
    This process continues until the user manually closes the window.

    :param input_queue: Queue receiving frames with detections from the detector
    """
    while True:
        if input_queue.empty():
            continue

        # Wait for frames from the detector
        frame, detections = input_queue.get()

        for (x, y, w, h) in detections:
            # Draw bounding boxes around detected motion
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Add current timestamp at the top-left corner
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 1)

        # Display the frame
        cv2.imshow("Video Stream", frame)

        # Allow user to quit manually by pressing 'q'
        if cv2.waitKey(33) & 0xFF == ord("q"):  # 30 fps instead of adding 1 as the parameter
            break

    # Close the window after exiting
    cv2.destroyAllWindows()
    # Note: In level one the program will works as long as the video runs and will
    # not turn off all the processes until the user closes the display
