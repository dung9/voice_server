from flask import Flask, request
import os
import wave

app = Flask(__name__)

@app.route('/')
def home():
    return "Server OK"

@app.route('/stt', methods=['POST'])
def stt():

    audio_data = request.data

    wav_file = "record.wav"

    with wave.open(wav_file, 'wb') as wf:

        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)

        wf.writeframes(audio_data)

    print("Saved:", wav_file)

    return "Nhan audio thanh cong"

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
