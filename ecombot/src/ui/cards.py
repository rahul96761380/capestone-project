def build_order_card(
    order_id: str,
    status: str,
    eta: str,
) -> str:

    return f"""
## Order Details

| Field | Value |
|---------|---------|
| Order ID | {order_id} |
| Status | {status} |
| Estimated Delivery | {eta} |
"""


def build_product_card(
    product_name: str,
    price: str,
    warranty: str,
    features: str,
) -> str:

    return f"""
## Product Details

| Field | Value |
|---------|---------|
| Product | {product_name} |
| Price | {price} |
| Warranty | {warranty} |
| Features | {features} |
"""


def build_comparison_card(
    product_a: str,
    product_a_price: str,
    product_a_warranty: str,
    product_b: str,
    product_b_price: str,
    product_b_warranty: str,
) -> str:

    return f"""
## Product Comparison

| Attribute | {product_a} | {product_b} |
|------------|------------|------------|
| Price | {product_a_price} | {product_b_price} |
| Warranty | {product_a_warranty} | {product_b_warranty} |
"""