from flask import Flask, request, Response
from openai import OpenAI
import tempfile
import wave

app = Flask(__name__)

client = OpenAI(
    api_key="OPENAI_API_KEY"
)

SAMPLE_RATE = 16000

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

@app.route('/stt', methods=['POST'])

def stt():

    try:

        pcm_data = request.data

        #====================================
        # PCM -> WAV
        #====================================

        wav_input = pcm_to_wav(pcm_data)

        #====================================
        # WHISPER
        #====================================

        audio_file = open(wav_input, "rb")

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
                    "Bạn là trợ lý AI nói tiếng Việt."
                },

                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        ai_text = chat.choices[0].message.content

        print("")
        print("AI:", ai_text)

        #====================================
        # OPENAI TTS WAV
        #====================================

        speech = client.audio.speech.create(

            model="gpt-4o-mini-tts",

            voice="alloy",

            input=ai_text,

            response_format="pcm"
        )

        pcm_audio = speech.content

        #====================================
        # STREAM PCM
        #====================================

        def generate():

            chunk_size = 1024

            for i in range(
                0,
                len(pcm_audio),
                chunk_size
            ):

                yield pcm_audio[
                    i:i+chunk_size
                ]

        return Response(

            generate(),

            mimetype=
            "application/octet-stream"
        )

    except Exception as e:

        print("ERROR:", e)

        return str(e), 500

#========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8080
    )
