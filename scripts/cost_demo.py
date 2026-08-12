"""
LR-19 Cost Routing Demonstration.

Runs five different prompt types through the cost-aware router
and compares the selected model's actual cost against the
most expensive configured model.
"""

from src.router import run_cost_routing


DEMO_PROMPTS = [
    (
        "Short factual",
        "What is the capital of France?",
    ),
    (
        "Long creative",
        (
            "Write a short creative story in about 150 words "
            "about a young scientist who discovers a hidden city "
            "under the ocean. Include one character, a short dialogue, "
            "and a surprising ending."
        ),
    ),
    (
        "Code generation",
        (
            "Write a Python program that reads a CSV dataset, "
            "cleans missing values, calculates basic statistics, "
            "and explains the code step by step."
        ),
    ),
    (
        "Reasoning",
        (
            "Compare supervised and unsupervised machine learning. "
            "Analyze their advantages, disadvantages, and explain "
            "which approach is more suitable for customer "
            "segmentation and why."
        ),
    ),
    (
        "Summarization",
        (
            "Summarize the following text in a few clear sentences: "
            "Artificial intelligence is a field of computer science "
            "that focuses on creating systems capable of performing "
            "tasks that normally require human intelligence, including "
            "learning, reasoning, perception, and decision-making."
        ),
    ),
]


def main():
    """Run the five-prompt LR-19 demonstration."""

    results = []

    print("=" * 70)
    print("LR-19 COST-ROUTING DEMONSTRATION")
    print("=" * 70)

    for prompt_type, prompt in DEMO_PROMPTS:

        print(f"\n[{prompt_type}]")
        print(f"Prompt: {prompt}")

        try:
            result = run_cost_routing(prompt)

            results.append(
                {
                    "type": prompt_type,
                    "complexity": result["complexity"],
                    "provider": result["provider"],
                    "model": result["model"],
                    "actual_cost": result["actual_cost"],
                    "comparison_cost": result["comparison_cost"],
                    "savings": result["estimated_savings"],
                    "status": "success",
                }
            )

        except Exception as error:

            print(f"ERROR: {error}")

            results.append(
                {
                    "type": prompt_type,
                    "complexity": "-",
                    "provider": "-",
                    "model": "-",
                    "actual_cost": None,
                    "comparison_cost": None,
                    "savings": None,
                    "status": "failed",
                }
            )

    print("\n")
    print("=" * 110)
    print("LR-19 COST COMPARISON SUMMARY")
    print("=" * 110)

    print(
        f"{'Type':<18}"
        f"{'Complexity':<12}"
        f"{'Provider':<10}"
        f"{'Actual Cost':<16}"
        f"{'Expensive Cost':<18}"
        f"{'Savings':<16}"
        f"{'Status':<10}"
    )

    print("-" * 110)

    for result in results:

        actual = (
            f"${result['actual_cost']:.8f}"
            if result["actual_cost"] is not None
            else "-"
        )

        comparison = (
            f"${result['comparison_cost']:.8f}"
            if result["comparison_cost"] is not None
            else "-"
        )

        savings = (
            f"${result['savings']:.8f}"
            if result["savings"] is not None
            else "-"
        )

        print(
            f"{result['type']:<18}"
            f"{result['complexity']:<12}"
            f"{result['provider']:<10}"
            f"{actual:<16}"
            f"{comparison:<18}"
            f"{savings:<16}"
            f"{result['status']:<10}"
        )


if __name__ == "__main__":
    main()