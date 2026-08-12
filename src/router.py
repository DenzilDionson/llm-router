"""
Cost-aware routing and prompt complexity classification.

Classifies prompts into simple, moderate, or complex,
then selects an appropriate model based on the routing
configuration in configs/models.yaml.
"""

import re
import yaml


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
    """
    Check whether any keyword appears as a complete word
    rather than as part of another word.
    """

    for keyword in keywords:
        pattern = rf"\b{re.escape(keyword)}\b"

        if re.search(pattern, text):
            return True

    return False


def classify_prompt(prompt: str) -> str:
    """
    Classify a prompt as simple, moderate, or complex.

    Classification considers:
    - Prompt length
    - Programming requirements
    - Mathematical requirements
    - Reasoning requirements
    - Long-output requirements
    - Multiple requirements
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
        A dictionary containing:
        - complexity
        - provider
        - model
        - reasoning
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


if __name__ == "__main__":

    test_prompts = [
        "What is the capital of France?",

        "Explain how a neural network works.",

        (
            "Write a Python program to analyze a dataset "
            "and explain the algorithm step by step."
        ),

        (
            "Write a detailed report comparing machine learning "
            "algorithms, analyze their mathematical foundations, "
            "and implement examples in Python."
        ),
    ]

    for prompt in test_prompts:

        result = select_model(prompt)

        print(f"Prompt: {prompt}")
        print(f"Complexity: {result['complexity']}")
        print(f"Provider: {result['provider']}")
        print(f"Model: {result['model']}")
        print(f"Reasoning: {result['reasoning']}")
        print()