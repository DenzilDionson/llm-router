"""
Prompt Complexity Classifier

This module classifies prompts into:
- simple
- medium
- complex
"""

CODING_KEYWORDS = [
    "python",
    "java",
    "javascript",
    "sql",
    "api",
    "flask",
    "fastapi",
    "docker",
    "github",
    "program",
    "code",
]

REASONING_KEYWORDS = [
    "compare",
    "analyze",
    "analysis",
    "evaluate",
    "explain",
    "reason",
    "difference",
    "advantages",
    "disadvantages",
]

MULTISTEP_KEYWORDS = [
    "build",
    "create",
    "implement",
    "design",
    "step by step",
    "complete",
    "project",
]


def score_prompt(prompt):
    """
    Calculate a complexity score.
    """

    prompt = prompt.lower()
    score = 0
    words = prompt.split()

    # Prompt length
    if len(words) > 20:
        score += 2
    elif len(words) > 10:
        score += 1

    # Coding keywords
    for keyword in CODING_KEYWORDS:
        if keyword in prompt:
            score += 1

    # Reasoning keywords
    for keyword in REASONING_KEYWORDS:
        if keyword in prompt:
            score += 1

    # Multi-step keywords
    for keyword in MULTISTEP_KEYWORDS:
        if keyword in prompt:
            score += 1

    return score


def classify_prompt(prompt):
    """
    Return one of:
    - simple
    - medium
    - complex
    """

    score = score_prompt(prompt)

    if score <= 2:
        return "simple"
    elif score <= 5:
        return "medium"
    else:
        return "complex"