import os

from litellm import Router

FAST_MODEL = "openrouter/google/gemini-2.5-flash"
DEEP_MODEL = "openrouter/google/gemini-2.5-pro"


def build_router():

    return Router(
        model_list=[
            {
                "model_name": "fast-faq",
                "litellm_params": {
                    "model": FAST_MODEL,
                    "api_key": os.getenv("OPENROUTER_API_KEY"),
                },
            },
            {
                "model_name": "deep-support",
                "litellm_params": {
                    "model": DEEP_MODEL,
                    "api_key": os.getenv("OPENROUTER_API_KEY"),
                },
            },
        ],
        fallbacks=[
            {
                "fast-faq": ["deep-support"]
            }
        ],
    )


router = build_router()

def classify_query(query: str):

    query = query.lower()

    deep_keywords = [
        "compare",
        "recommend",
        "best",
        "refund",
        "complaint",
        "issue",
        "problem",
        "multiple",
    ]

    if any(word in query for word in deep_keywords):
        return "deep-support"

    return "fast-faq"