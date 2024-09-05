# main.py
import threading
from flask import Flask
from video_processing import VideoProcessor
from audio_processing import AudioProcessor
from web_server import setup_routes

app = Flask(__name__)

def main():
    video_processor = VideoProcessor()
    audio_processor = AudioProcessor()

    # Start video processing thread
    video_thread = threading.Thread(target=video_processor.process_video)
    video_thread.daemon = True
    video_thread.start()

    # Setup Flask routes
    setup_routes(app, video_processor, audio_processor)

    # Run Flask app
    app.run(host="0.0.0.0", port="5000", debug=True, threaded=True, use_reloader=False)

    # Cleanup
    video_processor.release()

if __name__ == "__main__":
    main()

# video_processing.py
import cv2
import dlib
import numpy as np
from collections import deque
from scipy.spatial import distance as dist
import time

class VideoProcessor:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.output_frame = None
        self.video_lock = threading.Lock()
        
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        
        self.prev_gray = None
        self.face_motions = {}
        self.last_check_time = time.time()
        
        # Constants
        self.LEFT_EYE_INDICES = [36, 37, 38, 39, 40, 41]
        self.RIGHT_EYE_INDICES = [42, 43, 44, 45, 46, 47]
        self.GAZE_THRESHOLD = 0.25
        self.HISTORY_LENGTH = 5
        self.EYE_AR_THRESH = 0.2
        self.CHECK_INTERVAL = 3
        self.PICTURE_THRESHOLD = 5

    def eye_aspect_ratio(self, eye):
        # Implementation of eye_aspect_ratio function

    def get_eye_center(self, landmarks, eye_indices):
        # Implementation of get_eye_center function

    def detect_gaze(self, landmarks):
        # Implementation of detect_gaze function

    def detect_bounding_box(self, vid):
        # Implementation of detect_bounding_box function

    def process_frame(self, frame):
        # Implementation of process_frame function

    def generate(self):
        # Implementation of generate function

    def process_video(self):
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                break
            
            frame = self.process_frame(frame)

            with self.video_lock:
                self.output_frame = frame.copy()

    def release(self):
        self.video_capture.release()

# audio_processing.py
import sounddevice as sd
import soundfile as sf
import wave
import numpy as np
import queue

class AudioProcessor:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.audio_stream = None
        self.fs = 44100  # Sample rate

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Status: {status}")
        self.audio_queue.put(indata.copy())

    def save_to_wav(self, filename):
        # Implementation of save_to_wav function

    def start_recording(self):
        self.audio_stream = sd.InputStream(callback=self.audio_callback, channels=1, samplerate=self.fs)
        self.audio_stream.start()

    def stop_recording(self):
        if self.audio_stream:
            self.audio_stream.stop()
            self.audio_stream.close()
        self.save_to_wav("demo.wav")

    def ask_question(self):
        data, fs = sf.read("./questions/q1.wav")
        sd.play(data, fs)
        return "Question asked"

# web_server.py
from flask import Response, render_template, jsonify
import threading

def setup_routes(app, video_processor, audio_processor):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/video_feed')
    def video_feed():
        return Response(video_processor.generate(),
            mimetype = "multipart/x-mixed-replace; boundary=frame")

    @app.route('/start_recording', methods=['POST'])
    def start_recording_route():
        threading.Thread(target=audio_processor.start_recording).start()
        return jsonify({'message': 'Recording started'})

    @app.route('/stop_recording', methods=['POST'])
    def stop_recording_route():
        threading.Thread(target=audio_processor.stop_recording).start()
        return jsonify({'message': 'Recording stopped'})

    @app.route('/ask_question', methods=['GET'])
    def ask_question_route():
        return jsonify({'message': audio_processor.ask_question()})