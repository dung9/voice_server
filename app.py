from flask import Flask, request
import os
import wave

app = Flask(__name__)

@app.route('/')
def home():
    return "Server OK"

@app.route('/stt', methods=['POST'])
def stt():

    try:

        audio_data = request.data

        print("Audio size:", len(audio_data))

        if len(audio_data) == 0:
            return "No audio", 400

        wav_file = "record.wav"

        with wave.open(wav_file, 'wb') as wf:

            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)

            wf.writeframes(audio_data)

        print("Saved WAV OK")

        return "Audio received OK"

    except Exception as e:

        print("ERROR:", str(e))

        return str(e), 500


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
