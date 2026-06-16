import asyncio

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from ecombot.src.agents.support_agent import support_agent
from ecombot.src.agents.sales_agent import sales_agent

load_dotenv()

_MODEL = "openrouter/google/gemini-2.5-flash"

APP_NAME = "ecombot"
USER_ID = "orchestrator-user"


async def _run_specialist(agent: LlmAgent, request: str) -> str:
    """
    Run a specialist agent in its own session and
    return the final response text.
    """

    session_service = InMemorySessionService()

    session_id = f"{agent.name}-session"

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )

    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=request)],
    )

    reply = ""

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=user_message,
    ):
        if event.is_final_response():
            reply = event.content.parts[0].text or ""

    return reply.strip()


async def delegate_to_support_agent(request: str) -> str:
    """
    Delegate support-related requests.

    Use for:
    - Orders
    - Delivery
    - Returns
    - Refunds
    - Complaints
    - Inventory checks
    """

    return await _run_specialist(
        support_agent,
        request,
    )


async def delegate_to_sales_agent(request: str) -> str:
    """
    Delegate sales-related requests.

    Use for:
    - Product recommendations
    - Product comparisons
    - Product discovery
    - Product information
    """

    return await _run_specialist(
        sales_agent,
        request,
    )


_ORCHESTRATOR_PROMPT = """
You are eComBot Orchestrator.

You coordinate two specialist agents:

1. Support Agent
2. Sales Agent

Support Agent handles:
- Order status
- Delivery issues
- Returns
- Refunds
- Complaints
- Inventory availability
- Warranty and support policies

Sales Agent handles:
- Product recommendations
- Product comparisons
- Product discovery
- Product information
- Product FAQs

Routing Rules:

- If a request is only about orders, support,
  inventory, refunds, returns, or delivery,
  delegate to Support Agent.

- If a request is only about products,
  recommendations, comparisons, or shopping,
  delegate to Sales Agent.

- If a request needs both specialists,
  delegate to Support Agent first and then
  Sales Agent.

- Combine specialist responses into a single
  customer-friendly answer.

- Never invent information yourself.

- Use specialist responses as the source
  of truth.
""".strip()


orchestrator_agent = LlmAgent(
    name="orchestrator_agent",
    model=LiteLlm(model=_MODEL),
    instruction=_ORCHESTRATOR_PROMPT,
    tools=[
        delegate_to_support_agent,
        delegate_to_sales_agent,
    ],
)

root_agent = orchestrator_agent