import cv2
import numpy as np

def get_face_detector():
    return cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def get_eye_detector():
    return cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def calculate_eye_aspect_ratio(eye):
    width = np.linalg.norm(np.array(eye[0]) - np.array(eye[1]))
    height = np.linalg.norm(np.array(eye[0]) - np.array(eye[1]))
    ear = height / width
    return ear

def detect_liveness(frame, face_detector, eye_detector, threshold=0.2):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) == 0:
        return False, "No face detected"
    
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        eyes = eye_detector.detectMultiScale(roi_gray)
        
        if len(eyes) < 2:
            return False, "Both eyes not detected"
        
        ears = []
        for (ex, ey, ew, eh) in eyes[:2]:  # Consider only the first two detected eyes
            eye = [(ex, ey), (ex+ew, ey), (ex, ey+eh), (ex+ew, ey+eh)]
            ear = calculate_eye_aspect_ratio(eye)
            ears.append(ear)
        
        avg_ear = sum(ears) / len(ears)
        
        if avg_ear > threshold:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            return True, f"Liveness detected (EAR: {avg_ear:.2f})"
        else:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            return False, f"Possible printed image (EAR: {avg_ear:.2f})"

def main():
    cap = cv2.VideoCapture(0)
    face_detector = get_face_detector()
    eye_detector = get_eye_detector()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        is_live, message = detect_liveness(frame, face_detector, eye_detector)
        
        cv2.putText(frame, f"Live: {is_live}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, message, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.imshow('Liveness Detection', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()