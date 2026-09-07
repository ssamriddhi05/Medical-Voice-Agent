import edge_tts
import asyncio
import os
import uuid


async def generate_speech(text, output_file):
    communicate = edge_tts.Communicate(
        text=text,
        voice="en-US-AriaNeural"
    )

    await communicate.save(output_file)


def text_to_speech(text):
    """
    Converts text into speech and returns MP3 audio as bytes.
    """

    output_file = f"medical_response_{uuid.uuid4().hex}.mp3"

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:

        # Generate speech
        loop.run_until_complete(
            generate_speech(text, output_file)
        )

        # Check file exists
        if not os.path.exists(output_file):
            raise FileNotFoundError(
                "TTS audio file was not created."
            )

        # Check file size
        file_size = os.path.getsize(output_file)

        print("TTS file:", output_file)
        print("TTS file size:", file_size, "bytes")

        if file_size == 0:
            raise ValueError(
                "TTS generated an empty audio file."
            )

        # Read audio
        with open(output_file, "rb") as f:
            audio_bytes = f.read()

        return audio_bytes

    finally:

        # Close event loop
        loop.close()

        # Delete temporary file
        if os.path.exists(output_file):
            os.remove(output_file)