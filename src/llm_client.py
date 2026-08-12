import yaml
from litellm import completion
from dotenv import load_dotenv
from src.exceptions import ProviderError

load_dotenv()


def load_config(path="configs/models.yaml"):
    """Load the shared model configuration."""

    with open(path, "r") as file:
        return yaml.safe_load(file)


CONFIG = load_config()


def calculate_cost(
    provider_config,
    tokens_in,
    tokens_out,
):
    """
    Calculate the response cost using the configured
    input and output token prices.
    """

    input_cost = (
        tokens_in / 1000
    ) * provider_config["cost_per_1k_input"]

    output_cost = (
        tokens_out / 1000
    ) * provider_config["cost_per_1k_output"]

    return input_cost + output_cost


def call_llm(prompt: str, provider: str = "groq"):
    """
    Calls the specified provider's model using the shared config.

    Returns:
        provider
        model
        text
        cost
        tokens_in
        tokens_out
    """

    provider_config = CONFIG["providers"].get(provider)

    if not provider_config:
        raise ValueError(
            f"Unknown provider: {provider}"
        )

    model = provider_config["model"]

    try:
        response = completion(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

    except Exception as error:
        raise ProviderError(
            f"{provider} failed: {error}"
        ) from error

    usage = response.usage

    tokens_in = usage.prompt_tokens
    tokens_out = usage.completion_tokens

    # Try to get the actual cost reported by LiteLLM.
    cost = response._hidden_params.get(
        "response_cost",
        None,
    )

    # If LiteLLM does not provide the cost,
    # calculate it using our models.yaml pricing.
    if cost is None:
        cost = calculate_cost(
            provider_config,
            tokens_in,
            tokens_out,
        )

    return {
        "provider": provider,
        "model": model,
        "text": response.choices[0].message.content,
        "cost": cost,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
    }