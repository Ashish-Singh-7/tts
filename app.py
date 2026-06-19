from flask import Flask, render_template, request
from gtts import gTTS
from io import BytesIO
from langdetect import detect
import base64

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    text = request.form["text"]

    try:
        lang = detect(text)
    except:
        lang = "en"

    if lang == "hi":
        tts = gTTS(text=text, lang="hi")
    else:
        tts = gTTS(text=text, lang="en", tld="co.in")

    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)

    audio_data = base64.b64encode(
        mp3_fp.getvalue()
    ).decode()

    return render_template(
        "index.html",
        audio_data=audio_data
    )

if __name__ == "__main__":
    app.run(debug=True)