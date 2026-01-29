import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="cgi")
import cgi
import cv2
import numpy as np
from base64 import b64decode
import os

# Load Haar cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Known faces directory (authorized students)
KNOWN_FACES_DIR = "students"

def is_authorized_face(face_img, email):
    """Check if face belongs to authorized student"""
    try:
        # Load student reference image
        student_path = os.path.join(KNOWN_FACES_DIR, f"{email}.jpg")
        if not os.path.exists(student_path):
            return False
        
        student_img = cv2.imread(student_path)
        if student_img is None:
            return False
        
        # Simple pixel difference (works for frontal faces)
        face_gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        student_gray = cv2.cvtColor(student_img, cv2.COLOR_BGR2GRAY)
        
        # Resize both to same size for comparison
        face_resized = cv2.resize(face_gray, (100, 100))
        student_resized = cv2.resize(student_gray, (100, 100))
        
        # Calculate difference
        diff = cv2.absdiff(face_resized, student_resized)
        mean_diff = np.mean(diff)
        
        # Lower difference = better match
        return mean_diff < 15  # Threshold for match
    except:
        return False

# Get CGI form data
formdata = cgi.FieldStorage()
thief_detected = 0
email = formdata.getvalue("email", "")

image_data = formdata.getvalue("current_image")

if image_data:
    try:
        # Decode base64 image
        header, encoded = image_data.split(",", 1)
        data = b64decode(encoded)
        
        with open("current_frame.png", "wb") as f:
            f.write(data)
        
        # Load and process frame
        frame = cv2.imread("current_frame.png")
        frame = cv2.resize(frame, (640, 480))  # Resize for speed
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(50, 50))
        
        thief_alert = False
        
        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            
            # THIEF LOGIC 1: Unknown person (no email or not authorized)
            if not email or not is_authorized_face(face_img, email):
                color = (0, 0, 255)  # RED = THIEF
                label = "🚨 THIEF DETECTED"
                thief_alert = True
            else:
                color = (0, 255, 0)  # GREEN = AUTHORIZED
                label = "✅ Authorized"
            
            # Draw detection
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        # Save evidence
        cv2.imwrite("thief_detection_result.png", frame)
        
        if thief_alert:
            thief_detected = 1
            
    except Exception as e:
        print(f"Error processing image: {e}")

# CGI Response
print("Content-Type: text/html\n")

if thief_detected == 1:
    print("""
    <script>
    alert('🚨 THIEF DETECTED! 🚨\\nUnknown face captured!\\nCheck thief_detection_result.png');
    // Alarm sound
    new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NE').play();
    </script>
    """)
elif faces:
    print("<script>alert('👤 Face detected but authorized')</script>")
else:
    print("<script>alert('👀 No faces detected')</script>")

print()
