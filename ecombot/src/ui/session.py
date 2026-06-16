import chainlit as cl


def save_last_order(order_id: str) -> None:
    """Store the most recently used order ID."""
    cl.user_session.set(
        "last_order_id",
        order_id,
    )


def get_last_order() -> str | None:
    """Retrieve the last order ID."""
    return cl.user_session.get(
        "last_order_id"
    )


def save_customer_name(name: str) -> None:
    """Store customer name."""
    cl.user_session.set(
        "customer_name",
        name,
    )


def get_customer_name() -> str | None:
    """Retrieve customer name."""
    return cl.user_session.get(
        "customer_name"
    )


def save_last_product(product: str) -> None:
    """Store most recently discussed product."""
    cl.user_session.set(
        "last_product",
        product,
    )


def get_last_product() -> str | None:
    """Retrieve most recently discussed product."""
    return cl.user_session.get(
        "last_product"
    )