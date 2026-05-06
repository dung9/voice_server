from flask import Flask, request
import whisper

app = Flask(__name__)

model = whisper.load_model("base")

@app.route('/stt', methods=['POST'])
def stt():

    with open("record.wav", "wb") as f:
        f.write(request.data)

    result = model.transcribe(
        "record.wav",
        language='vi'
    )

    text = result["text"]

    print(text)

    return text

app.run(host="0.0.0.0", port=5000)
