from flask import Flask, request
import whisper
import os

app = Flask(__name__)

print("Loading Whisper model...")
model = whisper.load_model("base")

@app.route('/stt', methods=['POST'])
def stt():

    audio_file = request.files['audio']

    save_path = "record.wav"

    audio_file.save(save_path)

    print("Audio saved")

    result = model.transcribe(
        save_path,
        language='vi'
    )

    text = result["text"]

    print("TEXT:", text)

    return text

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000
    )
