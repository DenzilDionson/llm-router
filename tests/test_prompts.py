"""
Shared prompt set for evaluating the LLM Router.

These prompts cover different levels of complexity:
- Simple
- Moderate
- Complex
"""

TEST_PROMPTS = [
    # -------------------------------------------------
    # Simple prompts
    # -------------------------------------------------

    "What is Python?",

    "What is the capital of Sri Lanka?",

    "Say hello in one sentence.",

    "What is 10 + 25?",

    "Define artificial intelligence in one sentence.",


    # -------------------------------------------------
    # Moderate prompts
    # -------------------------------------------------

    "Explain the difference between Python lists and tuples.",

    "What are the main benefits of using cloud computing?",

    "Explain how an API works with a simple example.",

    "What is machine learning and how is it different from traditional programming?",

    "Explain the purpose of Git branches in software development.",


    # -------------------------------------------------
    # Complex prompts
    # -------------------------------------------------

    """
    Explain how a failover system works in an LLM router.
    Include the role of retries, fallback providers, timeouts,
    and error handling.
    """,

    """
    Compare cost-aware routing and failover routing in an
    LLM application. Explain how they can work together
    in a production system.
    """,

    """
    Write a Python function that calculates the total cost
    of an LLM request using input tokens, output tokens,
    input cost per 1,000 tokens, and output cost per
    1,000 tokens.
    """,

    """
    Design a simple architecture for an LLM router that
    supports multiple providers, automatic failover,
    cost-aware model selection, logging, and monitoring.
    Explain the purpose of each component.
    """,

    """
    Explain how you would test an LLM routing system using
    mocked provider failures. Include tests for successful
    requests, timeouts, retries, fallback behaviour,
    and complete provider failure.
    """
]