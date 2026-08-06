"""
Failover routing logic for the LLM Router.
"""

import yaml
import time

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
    If it fails, retry before automatically switching to fallback models.
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

    max_attempts = config["retry"]["max_attempts"]
    backoff = config["retry"]["backoff_seconds"]

    for model in model_order:

        for attempt in range(max_attempts + 1):

            try:
                print(f"Trying {model} (Attempt {attempt + 1})...")

                response = providers[model](prompt)

                print(f"{model} succeeded!")

                return response

            except ProviderError as error:

                print(f"{model} failed: {error}")

                if attempt < max_attempts:
                    print(f"Retrying in {backoff} seconds...\n")
                    time.sleep(backoff)

                else:
                    print(f"Moving to next provider...\n")

    raise Exception("All providers failed.")