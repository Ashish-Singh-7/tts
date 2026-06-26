from flask import Flask, render_template, request
from langdetect import detect
import edge_tts
import asyncio
import base64

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/convert", methods=["POST"])
def convert():

    text = request.form["text"]
    gender = request.form["gender"]
    speed = request.form["speed"]
    style = request.form["style"]

    try:
        lang = detect(text)
    except:
        lang = "en"

    # Hindi Voices
    if lang == "hi":

        if gender == "male":
            voice = "hi-IN-MadhurNeural"
        else:
            voice = "hi-IN-SwaraNeural"

    # English Voices
    else:

        if style == "cheerful":
            voice = "en-US-JennyNeural"

        elif style == "friendly":
            voice = "en-US-AriaNeural"

        elif style == "excited":
            voice = "en-US-AnaNeural"

        elif style == "hopeful":
            voice = "en-US-BrandonNeural"

        elif style == "sad":
            voice = "en-US-EmmaNeural"

        else:
            if gender == "male":
                voice = "en-US-GuyNeural"
            else:
                voice = "en-US-JennyNeural"

    audio_bytes = asyncio.run(
        generate_audio(text, voice, speed)
    )

    audio_data = base64.b64encode(
        audio_bytes
    ).decode("utf-8")

    return render_template(
        "index.html",
        audio_data=audio_data,
        text=text,
        gender=gender,
        speed=speed,
        style=style
    )


async def generate_audio(text, voice, speed):

    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=speed
    )

    audio_data = b""

    async for chunk in communicate.stream():

        if chunk["type"] == "audio":
            audio_data += chunk["data"]

    return audio_data


if __name__ == "__main__":
    app.run(debug=True)