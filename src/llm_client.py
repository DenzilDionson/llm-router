import os
import yaml
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

def load_config(path="configs/models.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

CONFIG = load_config()

def call_llm(prompt: str, provider: str = "groq"):
    """
    Calls the specified provider's model using the shared config.
    Returns a dict with response text, cost, and token usage.
    """
    provider_config = CONFIG["providers"].get(provider)
    if not provider_config:
        raise ValueError(f"Unknown provider: {provider}")

    model = provider_config["model"]

    response = completion(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    cost = response._hidden_params.get("response_cost", None)
    usage = response.usage

    return {
        "provider": provider,
        "model": model,
        "text": response.choices[0].message.content,
        "cost": cost,
        "tokens_in": usage.prompt_tokens,
        "tokens_out": usage.completion_tokens,
    }