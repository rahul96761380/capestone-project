import asyncio
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

load_dotenv()

_MODEL = "openrouter/google/gemini-2.5-flash"
_INSTRUCTION = (Path(__file__).parent / "support_instruction_v1.txt").read_text().strip()

APP_NAME = "ecombot"
USER_ID = "user-1"
SESSION_ID = "session-1"


root_agent = LlmAgent(
    name="support_agent",
    model=LiteLlm(model=_MODEL),
    instruction=_INSTRUCTION,
)


async def main():
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    question = "Hi, what do you do?"

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=question)],
    )

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message,
    ):
        if event.is_final_response():
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())