from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Server OK"

@app.route('/stt', methods=['POST'])
def stt():

    audio_data = request.data

    size = len(audio_data)

    print("Audio size:", size)

    return f"Nhan thanh cong {size} bytes"

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
