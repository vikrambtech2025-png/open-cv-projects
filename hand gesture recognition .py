import cv2
import numpy as np

# Open the default camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream. Make sure your webcam is available and not in use.")
else:
    print("Webcam opened successfully. Press 'q' to quit the video feed.")

    while(True):
        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to grab frame.")
            break

        # Flip the frame horizontally for a mirrored view (optional)
        frame = cv2.flip(frame, 1)

        # Define the region of interest (ROI) - a square in the center
        # You can adjust these values to focus on a specific area
        h, w, _ = frame.shape
        roi_size = min(h, w) // 2
        x1 = (w - roi_size) // 2
        y1 = (h - roi_size) // 2
        x2 = x1 + roi_size
        y2 = y1 + roi_size
        roi = frame[y1:y2, x1:x2]

        # Draw the ROI rectangle on the original frame
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # Convert ROI to HSV color space
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        # Define range of skin color in HSV
        # These values are approximate and might need tuning
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)

        # Threshold the HSV image to get only skin color
        mask = cv2.inRange(hsv_roi, lower_skin, upper_skin)

        # Apply morphological operations to remove noise and close gaps
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=1)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Find the largest contour (assumed to be the hand)
            largest_contour = max(contours, key=cv2.contourArea)

            # If the contour area is significant, draw it
            if cv2.contourArea(largest_contour) > 1000: # Adjust this threshold as needed
                # Draw the contour on the ROI
                cv2.drawContours(roi, [largest_contour], -1, (0, 255, 0), 2)

                # Now, you can perform gesture recognition based on 'largest_contour'
                # For example, counting fingers, checking orientation, etc.
                # (This part is left for further implementation)

        # Display the frame
        cv2.imshow('Hand Detection', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and destroy all windows
    cap.release()
    cv2.destroyAllWindows()
    print("Webcam feed stopped.")