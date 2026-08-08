"""
Main request router for the LLM Router.
"""
from src.failover import run_with_fallback


if __name__ == "__main__":
    response = run_with_fallback("Hello, how are you?")
    print("\nFinal Response:")
    print(response)
