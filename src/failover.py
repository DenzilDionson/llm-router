"""
Failover routing logic for the LLM Router.
"""
import yaml

from src.providers import (
    call_groq,
    call_cohere,
    call_gemini,
)

from src.exceptions import ProviderError


def load_config():
    """Load the YAML configuration."""

    with open("configs/models.yaml", "r") as file:
        return yaml.safe_load(file)


def run_with_fallback(prompt: str) -> str:
    """
    Try the primary model first.
    If it fails, automatically switch to fallback models.
    """

    config = load_config()

    primary = config["models"]["primary"]
    fallbacks = config["fallbacks"]

    providers = {
        "groq": call_groq,
        "cohere": call_cohere,
        "gemini": call_gemini,
    }

    model_order = [primary] + fallbacks

    for model in model_order:
        try:
            print(f"Trying {model}...")

            response = providers[model](prompt)

            print(f"{model} succeeded!")

            return response

        except ProviderError as error:
            print(f"{model} failed: {error}")

    raise Exception("All providers failed.")