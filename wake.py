import sounddevice as sd
from openwakeword.model import Model
from loguru import logger
import time

# Load all default models
model = Model()

SAMPLE_RATE = 16000
CHUNK_SIZE = 1280


def wake_word_listener():
    print("Listening for wake word...")

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        blocksize=CHUNK_SIZE
    ) as stream:

        while True:
            audio, _ = stream.read(CHUNK_SIZE)

            audio = audio.flatten()

            prediction = model.predict(audio)
            
            # Check chosen wake word
            score = prediction["alexa"]

            if score > 0.8:
                logger.info(f"Wake word detected! Score: {score}")
                print("Wake word detected!")
                
                model.reset()

                # Tiny cooldown
                time.sleep(0.5)
                
                stream.stop()

                return True