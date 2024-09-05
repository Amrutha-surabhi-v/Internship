# import sounddevice as sd
# import soundfile as sf
# import wave
# import queue
# from pydub import AudioSegment
# import threading
# from flask import Flask, jsonify, render_template
# import os

# app = Flask(__name__)

# # Audio processing globals
# audio_queue = queue.Queue()
# audio_stream = None
# fs = 44100  # Sample rate
# WAV_FILE = 'demo.wav'
# MP3_FILE = 'demo.mp3'

# # Audio processing functions
# def save_to_wav(filename):
#     audio_data = []
#     while not audio_queue.empty():
#         audio_data.append(audio_queue.get())
#     if not audio_data:
#         print("No audio data to save.")
#         return 
    
#     audio_data = np.concatenate(audio_data, axis=0)
    
#     with wave.open(filename, 'wb') as wf:
#         wf.setnchannels(1)  # Mono
#         wf.setsampwidth(2)  # 16-bit
#         wf.setframerate(fs)
#         wf.writeframes(audio_data.tobytes())

# def convert_wav_to_mp3(wav_file, mp3_file):
#     sound = AudioSegment.from_wav(wav_file)
#     sound.export(mp3_file, format="mp3")
#     print(f"Converted {wav_file} to {mp3_file}")

# def audio_callback(indata, frames, time, status):
#     if status:
#         print(f"Status: {status}")
#     audio_queue.put(indata.copy())

# def start_audio_recording():
#     global audio_stream
#     audio_stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=fs)
#     audio_stream.start()

# def stop_audio_recording():
#     global audio_stream
#     if audio_stream:
#         audio_stream.stop()
#         audio_stream.close()
#     save_to_wav(WAV_FILE)
#     convert_wav_to_mp3(WAV_FILE, MP3_FILE)
#     os.remove(WAV_FILE)  # Optionally remove the intermediate WAV file

# def ask_question():
#     data, fs = sf.read("./questions/q1.wav")
#     sd.play(data, fs)
#     return "Question asked"

# # Flask routes
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/start_recording', methods=['POST'])
# def start_recording_route():
#     threading.Thread(target=start_audio_recording).start()
#     return jsonify({'message': 'Audio recording started'})

# @app.route('/stop_recording', methods=['POST'])
# def stop_recording_route():
#     threading.Thread(target=stop_audio_recording).start()
#     return jsonify({'message': 'Audio recording stopped and saved as MP3'})

# @app.route('/ask_question', methods=['GET'])
# def ask_question_route():
#     return jsonify({'message': ask_question()})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port="5000", debug=True,
#             threaded=True, use_reloader=Fals

