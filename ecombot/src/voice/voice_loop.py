import asyncio
import time

import numpy as np
import sounddevice as sd

from google.genai import types

from ecombot.agent import orchestrator_agent

from ecombot.src.voice.stt import OpenRouterSTT
from ecombot.src.voice.tts import OpenRouterTTS
from ecombot.src.voice.metrics import (
    VoiceMetrics,
    print_metrics
)

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService


SAMPLE_RATE = 16000


def record_audio(seconds=5):

    print("🎙 Speak...")

    audio = sd.rec(
        int(seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="float32"
    )

    sd.wait()

    print("✓ Recording complete")

    return audio.flatten()


async def ask_agent(runner, text):

    response_text = ""

    async for event in runner.run_async(
        user_id="voice-user",
        session_id="voice-session",
        new_message=types.Content(
            role="user",
            parts=[types.Part(text=text)]
        )
    ):

        if (
            event.is_final_response()
            and event.content
            and event.content.parts
        ):
            response_text = (
                event.content.parts[0].text
            )

    return response_text


async def main():

    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name="ecombot",
        user_id="voice-user",
        session_id="voice-session"
    )

    runner = Runner(
        agent=orchestrator_agent,
        app_name="ecombot",
        session_service=session_service
    )

    stt = OpenRouterSTT()
    tts = OpenRouterTTS()

    while True:

        audio = record_audio()

        stt_result = stt.transcribe(audio)

        print(
            f"\nUser: {stt_result.text}\n"
        )

        agent_start = time.perf_counter()

        response = await ask_agent(
            runner,
            stt_result.text
        )

        agent_ms = int(
            (time.perf_counter() - agent_start)
            * 1000
        )

        print(
            f"Bot: {response}\n"
        )

        tts_start = time.perf_counter()

        tts.speak(response)

        tts_ms = int(
            (time.perf_counter() - tts_start)
            * 1000
        )

        metrics = VoiceMetrics(
            stt_ms=stt_result.latency_ms,
            agent_ms=agent_ms,
            tts_ms=tts_ms
        )

        print_metrics(metrics)


if __name__ == "__main__":
    asyncio.run(main())