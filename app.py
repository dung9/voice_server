from flask import Flask

app = Flask(__name__)

@app.route('/')

def home():

    return "VOICE SERVER OK"

@app.route('/stt', methods=['POST'])

def stt():

    return "STT OK"
