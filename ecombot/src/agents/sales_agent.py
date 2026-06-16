import asyncio
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.agents.readonly_context import ReadonlyContext

from ecombot.src.rag.retriever import retrieve

load_dotenv()

_MODEL = "openrouter/google/gemini-2.5-flash"

_INSTRUCTION = (Path(__file__).parent / "sales_instruction.txt" ).read_text().strip()


def build_instruction(ctx: ReadonlyContext):

    query = ""

    if ctx.user_content and ctx.user_content.parts:
        query = "".join(
            part.text or ""
            for part in ctx.user_content.parts
            if part.text
        )

    chunks = retrieve(query)

    context = "\n".join(chunks) if chunks else "NO RELEVANT INFORMATION FOUND"

    return f"""
{_INSTRUCTION}

Retrieved Context:
{context}

Answer only using the retrieved context.

If no relevant information exists, say:
"I couldn't find that information in my current knowledge base."
"""


sales_agent = LlmAgent(
    name="sales_agent",
    model=LiteLlm(model=_MODEL),
    instruction=build_instruction,
)

root_agent = sales_agent


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
