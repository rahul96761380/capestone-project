import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT))

import chainlit as cl

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from ecombot.src.agents.orchestrator import orchestrator_agent
from ecombot.src.ui.cards import (
    build_order_card,
    build_product_card,
)
from ecombot.src.ui.session import (
    save_last_order,
    get_last_order,
)

APP_NAME = "ecombot"
USER_ID = "chainlit-user"


async def run_agent(query: str) -> str:
    runner = cl.user_session.get("runner")
    session_id = cl.user_session.get("session_id")

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=query)],
    )

    response_text = ""

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=user_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                response_text = (
                    event.content.parts[0].text or ""
                )

    return response_text


@cl.on_chat_start
async def on_chat_start():
    session_service = InMemorySessionService()

    session_id = str(uuid.uuid4())

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    runner = Runner(
        agent=orchestrator_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    cl.user_session.set("runner", runner)
    cl.user_session.set("session_id", session_id)

    await cl.Message(
        content="👋 Hello! I'm eComBot. How can I help you today?"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    query = message.content

    if query.lower().startswith("can i return"):
        last_order = get_last_order()

        if last_order:
            query = f"Can I return order {last_order}?"

    response_text = await run_agent(query)

    if "ord-001" in query.lower():
        save_last_order("ORD-001")

        await cl.Message(
            content=build_order_card(
                order_id="ORD-001",
                status="Shipped",
                eta="2026-06-20",
            )
        ).send()

        await cl.Message(
            content=response_text
        ).send()

        return

    product_keywords = [
        "recommend",
        "product",
        "headphone",
        "smartwatch",
    ]

    if any(k in query.lower() for k in product_keywords):
        await cl.Message(
            content=response_text,
            actions=[
                cl.Action(
                    name="headphones",
                    label="🎧 Headphones",
                    payload={}
                ),
                cl.Action(
                    name="smartwatch",
                    label="⌚ Smart Watch",
                    payload={}
                ),
            ],
        ).send()
        return

    await cl.Message(content=response_text).send()


@cl.action_callback("headphones")
async def headphones_callback(action):
    response = await run_agent(
        "Recommend wireless headphones"
    )

    await cl.Message(
        content=build_product_card(
            product_name="Wireless Headphones",
            price="₹4,999",
            warranty="1 Year",
            features="Bluetooth 5.3, Noise Cancellation, 30 Hour Battery",
        )
    ).send()

    await cl.Message(content=response).send()


@cl.action_callback("smartwatch")
async def smartwatch_callback(action):
    response = await run_agent(
        "Recommend smart watch"
    )

    await cl.Message(
        content=build_product_card(
            product_name="Smart Watch",
            price="₹2,999",
            warranty="6 Months",
            features="Heart Rate Monitoring, Sleep Tracking, Water Resistant",
        )
    ).send()

    await cl.Message(content=response).send()