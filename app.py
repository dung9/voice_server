from flask import Flask, request
from openai import OpenAI
import wave
import os

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

@app.route('/')
def home():
    return "Server OK"

@app.route('/stt', methods=['POST'])
def stt():

    try:

        audio_data = request.data

        print("Audio bytes:", len(audio_data))

        wav_file = "record.wav"

        # Save WAV
        with wave.open(wav_file, 'wb') as wf:

            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)

            wf.writeframes(audio_data)

        # Whisper STT
        with open(wav_file, "rb") as audio_file:

            transcript =
                client.audio.transcriptions.create(

                    model="whisper-1",

                    file=audio_file
                )

        text = transcript.text

        print("TEXT:", text)

        return text

    except Exception as e:

        print("ERROR:", str(e))

        return str(e), 500

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
