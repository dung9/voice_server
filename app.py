from flask import Flask
from openai import OpenAI
import os

app = Flask(__name__)

api_key = os.getenv("OPENAI_API_KEY")

print("API KEY:")
print(api_key)

client = OpenAI(
    api_key=api_key
)

@app.route('/')
def home():

    try:

        response = client.chat.completions.create(

            model="gpt-3.5-turbo",

            messages=[
                {
                    "role": "user",
                    "content": "hello"
                }
            ]

        )

        text = response.choices[0].message.content

        return "OPENAI OK: " + text

    except Exception as e:

        print(str(e))

        return str(e)

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
