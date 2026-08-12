"""
Cost-aware routing and prompt complexity classification.

The router:
1. Classifies the prompt.
2. Selects an appropriate model.
3. Estimates the input cost before the API call.
4. Calls the selected model.
5. Logs actual token usage and actual cost.
6. Compares the actual cost with the most expensive model.
"""

import re
import yaml

from litellm import token_counter

from src.llm_client import call_llm


CODE_KEYWORDS = {
    "code",
    "python",
    "javascript",
    "java",
    "program",
    "programming",
    "function",
    "algorithm",
    "debug",
    "debugging",
    "sql",
    "api",
    "class",
    "implement",
}

MATH_KEYWORDS = {
    "calculate",
    "equation",
    "mathematics",
    "math",
    "derive",
    "integral",
    "derivative",
    "probability",
    "statistics",
    "formula",
    "solve",
}

REASONING_KEYWORDS = {
    "analyze",
    "analyse",
    "compare",
    "evaluate",
    "reason",
    "justify",
    "critically",
}

LONG_OUTPUT_KEYWORDS = {
    "essay",
    "detailed",
    "comprehensive",
    "report",
    "documentation",
}


def load_config(path="configs/models.yaml"):
    """Load the shared model configuration."""

    with open(path, "r") as file:
        return yaml.safe_load(file)


def contains_keyword(text: str, keywords: set[str]) -> bool:
    """Check whether a keyword appears as a complete word."""

    for keyword in keywords:
        pattern = rf"\b{re.escape(keyword)}\b"

        if re.search(pattern, text):
            return True

    return False


def classify_prompt(prompt: str) -> str:
    """
    Classify a prompt as simple, moderate, or complex.
    """

    if not isinstance(prompt, str):
        raise TypeError("Prompt must be a string.")

    prompt_lower = prompt.lower().strip()

    if not prompt_lower:
        raise ValueError("Prompt cannot be empty.")

    words = prompt_lower.split()
    word_count = len(words)

    score = 0

    # Prompt length
    if word_count <= 10:
        score -= 2

    elif word_count <= 30:
        score += 1

    elif word_count <= 60:
        score += 2

    else:
        score += 3

    # Programming requirements
    if contains_keyword(prompt_lower, CODE_KEYWORDS):
        score += 3

    # Mathematical requirements
    if contains_keyword(prompt_lower, MATH_KEYWORDS):
        score += 2

    # Reasoning requirements
    if contains_keyword(prompt_lower, REASONING_KEYWORDS):
        score += 2

    reasoning_phrases = {
        "explain why",
        "step by step",
    }

    if any(
        phrase in prompt_lower
        for phrase in reasoning_phrases
    ):
        score += 2

    # Long / detailed output requirements
    if contains_keyword(prompt_lower, LONG_OUTPUT_KEYWORDS):
        score += 2

    # Multiple requirements
    requirement_words = {
        "and",
        "also",
        "then",
        "with",
        "including",
        "using",
    }

    requirement_count = sum(
        len(re.findall(rf"\b{re.escape(word)}\b", prompt_lower))
        for word in requirement_words
    )

    if requirement_count >= 3:
        score += 1

    # Explicit short-answer requests
    short_output_requests = {
        "one sentence",
        "in one sentence",
        "briefly",
        "in short",
        "short answer",
    }

    if any(
        phrase in prompt_lower
        for phrase in short_output_requests
    ):
        score -= 2

    # Final classification
    if score >= 5:
        return "complex"

    if score >= 1:
        return "moderate"

    return "simple"


def select_model(prompt: str) -> dict:
    """
    Select the appropriate model based on prompt complexity.

    Returns:
        complexity
        provider
        model
        reasoning
    """

    config = load_config()

    complexity = classify_prompt(prompt)

    routing = config.get("routing", {})
    providers = config.get("providers", {})

    provider = routing.get(complexity)

    if not provider:
        raise ValueError(
            f"No provider configured for complexity: {complexity}"
        )

    provider_config = providers.get(provider)

    if not provider_config:
        raise ValueError(
            f"Provider '{provider}' is not configured."
        )

    model = provider_config.get("model")

    if not model:
        raise ValueError(
            f"No model configured for provider: {provider}"
        )

    reasoning = (
        f"The prompt was classified as '{complexity}', "
        f"so the '{provider}' model was selected."
    )

    return {
        "complexity": complexity,
        "provider": provider,
        "model": model,
        "reasoning": reasoning,
    }


def estimate_input_tokens(prompt: str, model: str) -> int:
    """
    Estimate the number of input tokens using LiteLLM.
    """

    messages = [
        {
            "role": "user",
            "content": prompt,
        }
    ]

    return token_counter(
        model=model,
        messages=messages,
    )


def estimate_input_cost(
    prompt: str,
    provider: str,
    model: str,
) -> dict:
    """
    Estimate the input cost before making the API call.
    """

    config = load_config()

    provider_config = config["providers"][provider]

    input_tokens = estimate_input_tokens(prompt, model)

    cost_per_1k = provider_config["cost_per_1k_input"]

    estimated_cost = (
        input_tokens / 1000
    ) * cost_per_1k

    return {
        "input_tokens": input_tokens,
        "estimated_input_cost": estimated_cost,
    }


def get_most_expensive_provider() -> str:
    """
    Find the provider with the highest combined
    input and output cost.
    """

    config = load_config()

    providers = config["providers"]

    return max(
        providers,
        key=lambda provider: (
            providers[provider]["cost_per_1k_input"]
            + providers[provider]["cost_per_1k_output"]
        ),
    )


def calculate_comparison_cost(
    tokens_in: int,
    tokens_out: int,
    provider: str,
) -> float:
    """
    Calculate what the same token usage would cost
    using another provider's configured pricing.
    """

    config = load_config()

    provider_config = config["providers"][provider]

    input_cost = (
        tokens_in / 1000
    ) * provider_config["cost_per_1k_input"]

    output_cost = (
        tokens_out / 1000
    ) * provider_config["cost_per_1k_output"]

    return input_cost + output_cost


def run_cost_routing(prompt: str) -> dict:
    """
    Run the complete cost-aware routing process.

    Steps:
    1. Select model based on complexity.
    2. Estimate input cost.
    3. Call selected model.
    4. Record actual token usage and cost.
    5. Compare actual cost against the most expensive model.
    """

    selection = select_model(prompt)

    provider = selection["provider"]
    model = selection["model"]

    # -------------------------------------------------
    # Pre-call cost estimation
    # -------------------------------------------------

    estimate = estimate_input_cost(
        prompt,
        provider,
        model,
    )

    print("\n--- Pre-call Cost Estimate ---")
    print(f"Provider: {provider}")
    print(f"Model: {model}")
    print(f"Estimated input tokens: {estimate['input_tokens']}")
    print(
        "Estimated input cost: "
        f"${estimate['estimated_input_cost']:.8f}"
    )

    # -------------------------------------------------
    # Actual LLM call
    # -------------------------------------------------

    result = call_llm(
        prompt,
        provider=provider,
    )

    tokens_in = result["tokens_in"]
    tokens_out = result["tokens_out"]
    actual_cost = result["cost"]

    # -------------------------------------------------
    # Post-call cost comparison
    # -------------------------------------------------

    expensive_provider = get_most_expensive_provider()

    expensive_cost = calculate_comparison_cost(
        tokens_in,
        tokens_out,
        expensive_provider,
    )

    if actual_cost is None:
        savings = None
    else:
        savings = expensive_cost - actual_cost

    print("\n--- Post-call Cost Report ---")
    print(f"Actual input tokens: {tokens_in}")
    print(f"Actual output tokens: {tokens_out}")
    print(f"Actual cost: ${actual_cost}")
    print(f"Most expensive provider: {expensive_provider}")
    print(
        "Equivalent expensive-model cost: "
        f"${expensive_cost:.8f}"
    )

    if savings is not None:
        print(
            "Estimated savings: "
            f"${savings:.8f}"
        )

    return {
        "prompt": prompt,
        "complexity": selection["complexity"],
        "provider": provider,
        "model": model,
        "reasoning": selection["reasoning"],
        "estimated_input_tokens": estimate["input_tokens"],
        "estimated_input_cost": estimate["estimated_input_cost"],
        "actual_input_tokens": tokens_in,
        "actual_output_tokens": tokens_out,
        "actual_cost": actual_cost,
        "comparison_provider": expensive_provider,
        "comparison_cost": expensive_cost,
        "estimated_savings": savings,
        "response": result["text"],
    }


if __name__ == "__main__":

    prompt = (
        "Write a Python program to analyze a dataset "
        "and explain the algorithm step by step."
    )

    result = run_cost_routing(prompt)

    print("\n=== Final Cost Routing Result ===")

    for key, value in result.items():
        if key != "response":
            print(f"{key}: {value}")

    print("\nResponse:")
    print(result["response"])