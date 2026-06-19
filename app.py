from flask import Flask, render_template, request
from gtts import gTTS
from langdetect import detect, LangDetectException
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():

    text = request.form["text"].strip()

    if not text:
        return render_template(
            "index.html",
            error="Please enter some text."
        )

    try:
        lang = detect(text)
    except LangDetectException:
        lang = "hi"

    os.makedirs("static/audio", exist_ok=True)

    filepath = "static/audio/output.mp3"

    if lang == "hi":
        tts = gTTS(text=text, lang="hi")
    else:
        tts = gTTS(text=text, lang="en", tld="co.in")

    tts.save(filepath)

    return render_template(
        "index.html",
        audio=filepath,
        detected_language=lang
    )

if __name__ == "__main__":
    app.run(debug=True)