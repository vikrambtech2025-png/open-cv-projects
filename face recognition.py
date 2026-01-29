import cv2
import numpy as np

# Load the pre-trained face detection cascade (download if needed from OpenCV GitHub)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

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

        # Convert frame to grayscale (required for Haar cascades)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces using Haar cascade
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # Optional: Label the detection
            cv2.putText(frame, 'Face', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        # Display the frame
        cv2.imshow('Face Detection', frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and destroy all windows
    cap.release()
    cv2.destroyAllWindows()
    print("Webcam feed stopped.")
