"""
Provider implementations for supported LLM services.
"""
from src.llm_client import call_llm


def call_groq(prompt: str) -> str:
    """
    Call Groq through the shared LLM client.
    """
    result = call_llm(prompt, provider="groq")
    return result["text"]


def call_cohere(prompt: str) -> str:
    """
    Call Cohere through the shared LLM client.
    """
    result = call_llm(prompt, provider="cohere")
    return result["text"]


def call_gemini(prompt: str) -> str:
    """
    Call Gemini through the shared LLM client.
    """
    result = call_llm(prompt, provider="gemini")
    return result["text"]
