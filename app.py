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

        print("")
        print("========================")
        print("Audio Bytes:", len(audio_data))
        print("========================")

        wav_file = "record.wav"

        # save wav
        with wave.open(wav_file, 'wb') as wf:

            wf.setnchannels(1)

            wf.setsampwidth(2)

            wf.setframerate(8000)

            wf.writeframes(audio_data)

        print("WAV Saved")

        # Whisper STT
        with open(wav_file, "rb") as audio_file:

            transcript = client.audio.transcriptions.create(

                model="whisper-1",

                file=audio_file
            )

        text = transcript.text

        print("")
        print("========================")
        print("TEXT:", text)
        print("========================")

        # trả text về ESP32
        return text

    except Exception as e:

        print("")
        print("========================")
        print("ERROR:", str(e))
        print("========================")

        return str(e), 500


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
