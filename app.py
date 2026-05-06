from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Server OK"

@app.route('/stt', methods=['POST'])
def stt():

    audio_data = request.data

    print("Audio received")

    print("Size:", len(audio_data))

    return "OK ESP32"

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
