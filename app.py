from flask import Flask, request, Response
from openai import OpenAI
import tempfile
import wave
import asyncio
import edge_tts
from pydub import AudioSegment

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
# TTS
#========================================

async def generate_tts(text, mp3_path):

    communicate = edge_tts.Communicate(

        text,

        voice="vi-VN-HoaiMyNeural"
    )

    await communicate.save(mp3_path)

#========================================
# Convert MP3 -> WAV PCM
#========================================

def convert_to_pcm_wav(mp3_file):

    wav_file = tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".wav"
    )

    audio = AudioSegment.from_mp3(mp3_file)

    audio = audio.set_frame_rate(16000)

    audio = audio.set_channels(1)

    audio = audio.set_sample_width(2)

    audio.export(

        wav_file.name,

        format="wav"
    )

    return wav_file.name

#========================================
# MAIN API
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
                    "Bạn là trợ lý AI nói tiếng Việt tự nhiên."
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
        # TTS
        #====================================

        mp3_file = tempfile.NamedTemporaryFile(

            delete=False,

            suffix=".mp3"
        )

        asyncio.run(

            generate_tts(
                ai_text,
                mp3_file.name
            )
        )

        #====================================
        # MP3 -> PCM WAV
        #====================================

        wav_output = convert_to_pcm_wav(
            mp3_file.name
        )

        #====================================
        # STREAM WAV
        #====================================

        def generate():

            with open(wav_output, "rb") as f:

                # skip WAV HEADER
                f.read(44)

                while True:

                    chunk = f.read(1024)

                    if not chunk:
                        break

                    yield chunk

        return Response(

            generate(),

            mimetype="application/octet-stream"
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
