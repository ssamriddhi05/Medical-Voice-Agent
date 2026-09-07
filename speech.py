import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import whisper


# -----------------------------
# Load Whisper
# -----------------------------

whisper_model = whisper.load_model("base")


# -----------------------------
# Record Audio
# -----------------------------

def record_audio(
    filename="medical_question.wav",
    duration=7,
    sample_rate=16000
):

    print("Recording...")

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    audio = np.squeeze(audio)

    wav.write(
        filename,
        sample_rate,
        audio
    )

    return filename


# -----------------------------
# Speech To Text
# -----------------------------

def speech_to_text(filename):

    result = whisper_model.transcribe(
        filename,
        fp16=False
    )

    text = result["text"].strip()

    return text