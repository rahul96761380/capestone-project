import io
import os
import time

import numpy as np
from openai import OpenAI


class STTResult:
    def __init__(self, text, latency_ms, confidence=1.0):
        self.text = text
        self.latency_ms = latency_ms
        self.confidence = confidence


class OpenRouterSTT:

    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )

    def transcribe(self, audio: np.ndarray):

        start = time.perf_counter()

        audio_int16 = (audio * 32767).astype("int16")

        buffer = io.BytesIO(audio_int16.tobytes())
        buffer.name = "audio.wav"

        result = self.client.audio.transcriptions.create(
            model="openai/whisper-1",
            file=buffer
        )

        latency_ms = int(
            (time.perf_counter() - start) * 1000
        )

        return STTResult(
            text=result.text,
            latency_ms=latency_ms,
            confidence=1.0
        )