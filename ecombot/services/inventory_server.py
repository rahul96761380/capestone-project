import time

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "ecombot-inventory",
    host="127.0.0.1",
    port=8002,
)

INVENTORY = {
    "PRD-101": {
        "product_id": "PRD-101",
        "name": "Wireless Headphones",
        "stock": 25,
        "variants": ["Black", "Blue", "Silver"],
    },
    "PRD-102": {
        "product_id": "PRD-102",
        "name": "Smart Watch",
        "stock": 10,
        "variants": ["Black", "Rose Gold"],
    },
}


@mcp.tool()
def check_stock(product_id: str):

    if product_id == "TIMEOUT":
        time.sleep(10)

    product = INVENTORY.get(product_id.upper())

    if not product:
        return {
            "found": False,
            "message": f"Product '{product_id}' not found.",
        }

    return {
        "found": True,
        "product_id": product["product_id"],
        "name": product["name"],
        "stock": product["stock"],
    }


@mcp.tool()
def list_variants(product_id: str):

    product = INVENTORY.get(product_id.upper())

    if not product:
        return {
            "found": False,
            "message": f"Product '{product_id}' not found.",
        }

    return {
        "found": True,
        "product_id": product["product_id"],
        "name": product["name"],
        "variants": product["variants"],
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")