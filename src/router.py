from complexity import classify_prompt

MODEL_TIERS = {
    "simple": "llama-3.1-8b",
    "medium": "gemini-2.5-flash",
    "complex": "gemini-2.5-pro",
}


def select_model(prompt):
    """
    Select the most suitable model
    based on prompt complexity.
    """

    complexity = classify_prompt(prompt)

    return MODEL_TIERS[complexity]