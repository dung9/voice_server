from flask import Flask, request, send_file
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

app = Flask(__name__)

@app.route("/")
def home():
    return "ESP32 Voice Server OK"

@app.route("/voice", methods=["POST"])
def voice():

    audio = request.files["file"]

    input_file = "input.wav"
    output_file = "reply.mp3"

    audio.save(input_file)

    # STT
    with open(input_file, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )

    user_text = transcript.text

    print("USER:", user_text)

    # GPT
    chat = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Bạn là AI assistant cho ESP32."
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    )

    ai_reply = chat.choices[0].message.content

    print("AI:", ai_reply)

    # TTS
    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=ai_reply
    )

    with open(output_file, "wb") as f:
        f.write(speech.content)

    return send_file(output_file, mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)