import sounddevice as sd
from scipy.io.wavfile import write
import asyncio

from faster_whisper import WhisperModel

from voice import speak

from log import log_init

from llm import ask_llm

import time

from loguru import logger

import os


import sounddevice as sd
import numpy as np
import torch
from scipy.io.wavfile import write
from silero_vad import load_silero_vad, get_speech_timestamps


from wake import wake_word_listener


duration = 3
sample_rate = 16000
output_file = "voice.wav"


model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)



vad_model = load_silero_vad()



def listen():

    if os.path.exists(output_file):
        os.remove(output_file)

    print("Listening for speech...")

    duration = 8  # max recording window
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    audio = audio.flatten()

    # Convert to torch tensor
    audio_tensor = torch.tensor(audio)

    # Detect speech timestamps
    speech_timestamps = get_speech_timestamps(
        audio_tensor,
        vad_model,
        sampling_rate=sample_rate
    )

    if not speech_timestamps:
        print("No speech detected.")
        logger.warning("listen : No speech detected")
        return False

    # Trim to speech-only region
    start = speech_timestamps[0]["start"]
    end = speech_timestamps[-1]["end"]

    speech_audio = audio[start:end]

    # Convert back for whisper
    speech_audio_int16 = (speech_audio * 32767).astype(np.int16)

    write(output_file, sample_rate, speech_audio_int16)

    print("Speech captured.")
    logger.info("listen : Speech captured successfully")
    
    return True


def transcribe():
    print("Processing...")

    if not os.path.exists(output_file):
        logger.warning("transcribe : No audio file found")
        return ""

    segments, info = model.transcribe(output_file, language="en")
    segments = list(segments)

    print("Segments:", len(segments))

    text = " ".join(segment.text for segment in segments).lower().strip()

    if not text:
        logger.warning("transcribe : Empty transcript")
        print("No speech recognized.")
        return ""

    print("Detected language:", info.language)
    print("Final Command:", text)

    return text



def main():
    
    log_init()

    logger.warning("Acess : USER ACCESSES SPARKY - Session starts!!")
    while(True):
        wake_word_listener()


        if not listen():
            asyncio.run(speak("I didn't catch that"))
            print("I didn't catch that!")
            continue
        
        text = transcribe()

        if not text.strip():
            print("Noting in text - transcribed")
            continue
            

        logger.info(f"Transcript : Input Transcript - \"{text}\"")

        if "exit" in text or "quit" in text or "stop" in text or "bye" in text:
            logger.warning("exit : USER EXIT SPARKY - Sessions ends!!\n")
            print("Thanks for using, goodbye!!")
            asyncio.run(speak("Goodbye!"))
            break


        else:
            logger.info("LLM : Goes into LLM for intent and action")
            ask_llm(text)

        
        time.sleep(2)

        os.remove(output_file)


main()