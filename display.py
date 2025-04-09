import cv2
from datetime import datetime


def display_frames(input_queue):
    """
    Displays video frames with motion detection rectangles and a timestamp overlay.
    This process continues until the user manually closes the window.

    :param input_queue: Queue receiving frames with detections from the detector
    """
    while True:
        # Wait for the next item from the queue (sent by the detector)
        data = input_queue.get()

        # Check if the detector signaled termination
        # "END" is a sentinel value indicating no more frames will be sent
        if data == "END":
            print("[Display] Received END signal. Exiting.")
            break

        # Unpack the tuple into frame and list of motion detections
        # data is expected to be (frame, detections)
        frame, detections = data

        # For each detected motion region, apply Gaussian blur
        # Note: In Stage 1, detections were visualized using green bounding boxes.
        # In Stage 2, as per assignment requirements, we replace the visual indication
        # with a blur effect applied only in the display layer.
        # This ensures the original frame is not altered in earlier components
        # and maintains full separation between detection and presentation logic.
        for (x, y, w, h) in detections:
            # Extract the region of interest (ROI) based on
            # the bounding box
            roi = frame[y:y+h, x:x+w]

            # step 2 - Blurring algorithm
            # Apply Gaussian blur to the ROI
            # Why Gaussian Blur?
            # - Smooth, natural-looking result
            # - Preserves shape while masking detail
            # - Performs well in real-time (optimized in OpenCV)
            #  This Blurring algorithm works well when the ROI isn't so big
            #  (covering the whole picture for example) or if there are hundreds
            #  of detections per frame, in almost all cases this won't be a problem here
            #  but in extreme cases there are ways to improve the efficiency
            #  such as minimizing the kernel size
            blurred_roi = cv2.GaussianBlur(roi, (31, 31), 0)

            # Replace the original region with the blurred version
            frame[y:y+h, x:x+w] = blurred_roi

            # Draw bounding boxes around detected motion
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Add current timestamp at the top-left corner
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 1)

        # Display the frame
        cv2.imshow("Video Stream", frame)

        # Allow user to quit manually by pressing 'q'
        if cv2.waitKey(33) & 0xFF == ord("q"):  # 30 fps instead of adding 1 as the parameter
            print("[Display] Manual exit by user.")
            break

    # Close the window after exiting
    cv2.destroyAllWindows()
    # Note: In level one the program will works as long as the video runs and will
    # not turn off all the processes until the user closes the display
