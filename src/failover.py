"""
Failover routing logic for the LLM Router.
"""

import logging
import yaml
import time

from src.providers import (
    call_groq,
    call_cohere,
    call_gemini,
)

from src.exceptions import ProviderError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def load_config():
    """Load the YAML configuration."""

    with open("configs/models.yaml", "r") as file:
        return yaml.safe_load(file)


def run_with_fallback(prompt: str) -> str:
    """
    Try providers in the configured fallback chain.
    Retry each provider before moving to the next one.
    """

    config = load_config()
    start_time = time.time()

    providers = {
        "groq": call_groq,
        "cohere": call_cohere,
        "gemini": call_gemini,
    }

    # Read provider order from the shared configuration
    model_order = config["fallback_chain"]

    max_attempts = config["retry"]["max_attempts"]
    backoff = config["retry"]["backoff_seconds"]

    for model in model_order:

        for attempt in range(max_attempts + 1):

            try:
                logger.info(f"Trying {model} (Attempt {attempt + 1})")

                response = providers[model](prompt)

                logger.info(f"{model} succeeded")

                elapsed_time = time.time() - start_time
                logger.info(
                    f"Total response time: {elapsed_time:.2f} seconds"
                )

                return response

            except ProviderError as error:

                logger.error(f"{model} failed: {error}")

                if attempt < max_attempts:

                    logger.info(
                        f"Retrying in {backoff} seconds"
                    )

                    time.sleep(backoff)

                else:

                    logger.warning(
                        "Moving to next provider"
                    )

    raise Exception("All providers failed.")
