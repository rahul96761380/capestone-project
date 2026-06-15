from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "ecombot-orders",
    host="127.0.0.1",
    port=8001,
)
ORDERS = {
    "ORD-001": {
        "order_id": "ORD-001",
        "customer": "Rahul Sekar",
        "product": "Wireless Headphones",
        "status": "Shipped",
        "delivery_date": "2026-06-20",
    },
    "ORD-002": {
        "order_id": "ORD-002",
        "customer": "Priya Sharma",
        "product": "Smart Watch",
        "status": "Delivered",
        "delivery_date": "2026-06-10",
    },
}


def _not_found(order_id: str):
    return {
        "found": False,
        "order_id": order_id,
        "message": f"No order found with ID '{order_id}'",
    }


@mcp.tool()
def get_order_status(order_id: str):

    order = ORDERS.get(order_id.upper())

    if not order:
        return _not_found(order_id)

    return {
        "found": True,
        "order_id": order["order_id"],
        "status": order["status"],
        "delivery_date": order["delivery_date"],
    }


@mcp.tool()
def get_order_details(order_id: str):

    order = ORDERS.get(order_id.upper())

    if not order:
        return _not_found(order_id)

    return {
        "found": True,
        **order,
    }


@mcp.tool()
def cancel_order(order_id: str, confirm: bool = False):

    order = ORDERS.get(order_id.upper())

    if not order:
        return _not_found(order_id)

    if not confirm:
        return {
            "found": True,
            "status": "cancellation_pending",
            "message": (
                f"This will cancel order {order_id}. "
                "Call cancel_order again with confirm=True."
            ),
        }

    order["status"] = "Cancelled"

    return {
        "found": True,
        "order_id": order_id,
        "status": "Cancelled",
        "message": f"Order {order_id} cancelled successfully.",
    }


if __name__ == "__main__":
    print("Orders MCP Server starting...")
    mcp.run(transport="streamable-http")