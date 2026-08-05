"""
Provider implementations for supported LLM services.
"""
from src.exceptions import (
    TimeoutError,
    RateLimitError,
    EmptyResponseError,
)


def call_groq(prompt: str) -> str:
    """
    Simulate a request to the Groq API.
    """
    raise TimeoutError("Groq request timed out")


def call_cohere(prompt: str) -> str:
    """
    Simulate a request to the Cohere API.
    """
    return f"Cohere response: {prompt}"


def call_gemini(prompt: str) -> str:
    """
    Simulate a request to the Gemini API.
    """
    return f"Gemini response: {prompt}"
