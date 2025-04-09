import cv2

# How often to refresh the baseline frame (in number of frames)
# Note: Can be adjusted based on the video input
REFRESH_INTERVAL = 60  # ~2 seconds at 30 FPS


def detect_motion(input_queue, output_queue):
    """
    Processes frames from the input queue, detects motion regions, and
    sends the original frame along with bounding boxes to the display.
    This function runs until the streamer stops producing frames.

    :param input_queue: Queue receiving frames from the streamer
    :param output_queue: Queue sending frames and detections to the display
    """
    # Used as the baseline reference for motion detection
    first_frame = None
    frame_count = 0

    while True:
        # Receive frame from streamer
        # blocking call – waits for frame
        frame = input_queue.get()
        if frame is None:
            print("[Detector] Received None frame – skipping")
            continue
        frame_count += 1

        # Convert to grayscale to simplify processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        # Note: This is not The Blurring of step 2
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Store the first frame for comparison
        if first_frame is None:
            first_frame = gray
            continue

        # Refresh baseline frame every 100 frames (~3 sec)
        if frame_count % REFRESH_INTERVAL == 0:
            first_frame = gray

        # Compare current frame to baseline frame
        frame_delta = cv2.absdiff(first_frame, gray)

        # Generate binary mask and dilate it to fill in holes
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        # Show the binary mask of movement (for debugging)
        cv2.imshow("Motion Mask", thresh)
        cv2.waitKey(1)

        # Find contours around detected regions
        contours, _ = cv2.findContours(
            thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        detections = []
        # Filter out small movements
        for contour in contours:
            if cv2.contourArea(contour) < 100:
                continue

            # Store bounding boxes of motion
            (x, y, w, h) = cv2.boundingRect(contour)
            detections.append((x, y, w, h))

        # Send frame and detection list to the display
        output_queue.put((frame, detections))
