from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import speech_recognition as sr

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['audio']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return jsonify({"text": text})
        except sr.UnknownValueError:
            return jsonify({"error": "Speech Recognition could not understand audio"}), 400
        except sr.RequestError:
            return jsonify({"error": "Google Speech Recognition service failed"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)