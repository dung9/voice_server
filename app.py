from flask import Flask, request
import whisper
import os

app = Flask(__name__)

print("Loading Whisper model...")
model = whisper.load_model("tiny")

@app.route("/")
def home():
    return "Server OK"

@app.route("/stt", methods=["POST"])
def stt():

    with open("record.wav", "wb") as f:
        f.write(request.data)

    result = model.transcribe(
        "record.wav",
        language="vi"
    )

    text = result["text"]

    print("TEXT:", text)

    return text

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 8080))

    app.run(
        host="0.0.0.0",
        port=port
    )
