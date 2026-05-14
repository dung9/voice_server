from flask import Flask, request, Response
from openai import OpenAI
import tempfile
import wave
import os

print("SERVER STARTED")

app = Flask(__name__)

#========================================
# OPENAI
#========================================

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

SAMPLE_RATE = 16000

#========================================
# HOME
#========================================

@app.route('/')

def home():

    return "VOICE SERVER OK"

#========================================
# PCM -> WAV
#========================================

def pcm_to_wav(pcm_data):

    temp_wav = tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".wav"
    )

    with wave.open(
        temp_wav.name,
        'wb'
    ) as wf:

        wf.setnchannels(1)

        wf.setsampwidth(2)

        wf.setframerate(SAMPLE_RATE)

        wf.writeframes(pcm_data)

    return temp_wav.name

#========================================
# STT
#========================================

@app.route('/stt', methods=['POST'])

def stt():

    try:

        print("")
        print("========================")
        print("REQUEST RECEIVED")
        print("========================")

        pcm_data = request.data

        print("PCM SIZE:", len(pcm_data))

        #====================================
        # PCM -> WAV
        #====================================

        wav_input = pcm_to_wav(pcm_data)

        print("WAV CREATED")

        #====================================
        # WHISPER
        #====================================

        with open(wav_input, "rb") as audio_file:

            transcript = client.audio.transcriptions.create(

                model="whisper-1",

                file=audio_file
            )

        user_text = transcript.text

        print("")
        print("USER:", user_text)

        #====================================
        # GPT
        #====================================

        chat = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role": "system",
                    "content":
                    """
                    Bạn là trợ lý AI tiếng Việt.

                    Trả lời:
                    - ngắn gọn
                    - tự nhiên
                    - dưới 20 từ
                    """
                },

                {
                    "role": "user",
                    "content": user_text
                }
            ],

            max_tokens=60
        )

        ai_text = chat.choices[0].message.content

        print("")
        print("AI:", ai_text)

        #====================================
        # OPENAI TTS
        #====================================

        speech = client.audio.speech.create(

            model="gpt-4o-mini-tts",

            voice="nova",

            input=ai_text,

            response_format="pcm"
        )

        pcm_audio = speech.content

        print("")
        print("PCM AUDIO SIZE:", len(pcm_audio))

        #====================================
        # STREAM PCM
        #====================================

        def generate():

            chunk_size = 512

            for i in range(
                0,
                len(pcm_audio),
                chunk_size
            ):

                yield pcm_audio[
                    i:i + chunk_size
                ]

        return Response(

            generate(),

            mimetype=
            "application/octet-stream"
        )

    except Exception as e:

        print("")
        print("ERROR:", str(e))

        return str(e), 500

#========================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=8080,

        threaded=True
    )
