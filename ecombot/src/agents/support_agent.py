import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from ecombot.src.tools.order_tools import get_order_status, save_customer_name
from ecombot.src.rag.retriever import retrieve
from google.adk.agents.readonly_context import ReadonlyContext
from ecombot.src.routing import (
    classify_query,
    FAST_MODEL,
    DEEP_MODEL,
)
from google.adk.tools.mcp_tool import (
    McpToolset,
    StreamableHTTPConnectionParams,
)

load_dotenv()

print("OPENROUTER_API_KEY =", os.getenv("OPENROUTER_API_KEY"))

_MODEL = "openrouter/google/gemini-2.5-flash"
_INSTRUCTION = (Path(__file__).parent / "support_instruction_v3.txt").read_text().strip()

APP_NAME = "ecombot"
USER_ID = "user-1"
SESSION_ID = "session-1"

orders_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="http://127.0.0.1:8001/mcp",
        timeout=10,
    ),
)

inventory_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="http://127.0.0.1:8002/mcp",
        timeout=10,
    ),
)


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

support_agent = LlmAgent(
    name="support_agent",
    model=LiteLlm(model=FAST_MODEL),
    instruction=build_instruction,
    tools=[
        save_customer_name,
        orders_toolset,
        inventory_toolset,
    ],
)

root_agent = support_agent

deep_agent = LlmAgent(
    name="ecombot_deep",
    model=LiteLlm(model=DEEP_MODEL),
    instruction=build_instruction,
    tools=[
        get_order_status,
        save_customer_name,
    ]
)

"""
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

    question = "Hi, what do you do? and get me order status of ORD-001"

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
    """