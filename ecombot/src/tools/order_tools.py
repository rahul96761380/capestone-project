from typing import Any
from ecombot.services.db import query_one

from google.adk.tools import ToolContext

# ── Static data ────────────────────────────────────────────────────────────


_ORDERDATA: dict[str, dict[str, str]] = {
    "ORD-001": {
        "order_id": "ORD-001",
        "status": "Shipped",
        "eta": "5 Jun 2026",
        "carrier": "BlueDart",
    },
    "ORD-002": {
        "order_id": "ORD-002",
        "status": "Processing",
        "eta": "7 Jun 2026",
        "carrier": "DTDC",
    },
    "ORD-003": {
        "order_id": "ORD-003",
        "status": "Delivered",
        "eta": "Already delivered",
        "carrier": "FedEx",
    },
}


# ── Tool function ──────────────────────────────────────────────────────────

def get_order_status(
    order_id: str,
    tool_context: ToolContext,
):
    key = order_id.strip().upper()

    tool_context.state["last_order_id"] = key

    try:
        order = query_one(
            """
            SELECT order_id,
                   customer_name,
                   product_id,
                   order_status,
                   order_date
            FROM orders
            WHERE order_id=%s
            """,
            (key,),
        )

        if not order:
            return {
                "found": False,
                "error": f"Order {key} not found."
            }

        return {
            "found": True,
            **order
        }

    except Exception as e:
        print(f"Database error: {e}")
        return {
            "found": False,
            "error": str(e)
        }
    

def save_customer_name(
    customer_name: str,
    tool_context: ToolContext,
) -> dict[str, str]:

    name = customer_name.strip()

    tool_context.state["customer_name"] = name

    return {
        "saved": "true",
        "customer_name": name,
    }

    