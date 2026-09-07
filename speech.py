import whisper
import tempfile
import os


# =========================================================
# LOAD WHISPER MODEL
# =========================================================

whisper_model = whisper.load_model("base")


# =========================================================
# SAVE BROWSER AUDIO
# =========================================================

def save_audio(audio_bytes):
    """
    Saves audio bytes received from Streamlit
    into a temporary WAV file.
    """

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    temp_file.write(audio_bytes)
    temp_file.close()

    return temp_file.name


# =========================================================
# SPEECH TO TEXT
# =========================================================

def speech_to_text(audio_file):

    try:

        result = whisper_model.transcribe(
            audio_file,
            fp16=False
        )

        text = result["text"].strip()

        return text

    finally:

        # Delete temporary audio file
        if os.path.exists(audio_file):
            os.remove(audio_file)
