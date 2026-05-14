from flask import Flask, request, Response
from openai import OpenAI
import tempfile
import wave
import asyncio
import edge_tts

app = Flask(__name__)

client = OpenAI(
    api_key="OPENAI_API_KEY"
)

SAMPLE_RATE = 16000

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

async def text_to_speech(text, output):

    communicate = edge_tts.Communicate(

        text,

        voice="vi-VN-HoaiMyNeural"
    )

    await communicate.save(output)

#========================================

@app.route('/stt', methods=['POST'])

def stt():

    pcm_data = request.data

    wav_file = pcm_to_wav(pcm_data)

    #================ WHISPER ================

    audio_file = open(wav_file, "rb")

    transcript = client.audio.transcriptions.create(

        model="whisper-1",

        file=audio_file
    )

    user_text = transcript.text

    print("USER:", user_text)

    #================ GPT ====================

    chat = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[

            {
                "role": "system",
                "content": "Bạn là trợ lý AI nói tiếng Việt."
            },

            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    ai_text = chat.choices[0].message.content

    print("AI:", ai_text)

    #================ TTS ====================

    mp3_file = tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".mp3"
    )

    asyncio.run(

        text_to_speech(
            ai_text,
            mp3_file.name
        )
    )

    audio_bytes = open(
        mp3_file.name,
        "rb"
    ).read()

    return Response(

        audio_bytes,

        mimetype="audio/mpeg"
    )

#========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8080
    )
