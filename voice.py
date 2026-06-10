import edge_tts
import subprocess
import tempfile
import os

async def speak(text):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        filename = f.name

    try:
        await edge_tts.Communicate(
            text,
            "en-GB-SoniaNeural"
        ).save(filename)

        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", filename],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    finally:
        os.remove(filename)
