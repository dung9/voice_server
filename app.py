from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Server OK"

@app.route('/stt', methods=['POST'])
def stt():

    try:

        data = request.get_data()

        print("DATA LEN:", len(data))

        return "OK"

    except Exception as e:

        print(str(e))

        return str(e), 500

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
