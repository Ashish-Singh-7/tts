from flask import Flask, render_template, request, send_file
from gtts import gTTS
from io import BytesIO
from langdetect import detect

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
    mp3_fp.seek(0)

    return send_file(
        mp3_fp,
        mimetype="audio/mpeg",
        as_attachment=False,
        download_name="speech.mp3"
    )