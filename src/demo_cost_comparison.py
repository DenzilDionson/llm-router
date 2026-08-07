from complexity import classify_prompt
from router import select_model
from pricing import calculate_cost


PROMPTS = [
    "What is Python?",
    "Explain how REST APIs work.",
    "Compare Python and Java with examples.",
    "Build a complete Flask REST API using Docker and PostgreSQL. Explain every step.",
]


def estimate_tokens(prompt):
    """
    Simple token estimate for demonstration purposes.
    This is not an exact tokenizer.
    """

    words = len(prompt.split())

    return max(1, int(words * 1.3))


def get_pricing_model(model):
    """
    Map router model names to models available
    in the pricing table.
    """

    if model == "gemini-2.5-flash":
        return "gemini-2.0-flash"

    if model == "gemini-2.5-pro":
        return "gemini-2.0-flash"

    return model


def main():

    print("=" * 70)
    print("COST-AWARE ROUTING - COST COMPARISON DEMO")
    print("=" * 70)

    total_router_cost = 0
    total_single_model_cost = 0

    # Model used as the baseline for comparison
    baseline_model = "gemini-2.0-flash"

    for prompt in PROMPTS:

        # LR-7
        complexity = classify_prompt(prompt)

        # LR-11
        selected_model = select_model(prompt)

        # Map to an available pricing model
        pricing_model = get_pricing_model(selected_model)

        # Estimate tokens
        input_tokens = estimate_tokens(prompt)
        estimated_output_tokens = 300

        # LR-3 pricing calculation
        router_cost = calculate_cost(
            pricing_model,
            input_tokens,
            estimated_output_tokens,
        )

        # Calculate cost if every prompt used the baseline model
        baseline_cost = calculate_cost(
            baseline_model,
            input_tokens,
            estimated_output_tokens,
        )

        total_router_cost += router_cost
        total_single_model_cost += baseline_cost

        print()
        print("-" * 70)

        print("Prompt:")
        print(prompt)

        print()

        print("Complexity:")
        print(complexity)

        print()

        print("Selected model:")
        print(selected_model)

        print()

        print("Pricing model used:")
        print(pricing_model)

        print()

        print("Estimated input tokens:")
        print(input_tokens)

        print()

        print("Estimated output tokens:")
        print(estimated_output_tokens)

        print()

        print("Cost using cost-aware routing:")
        print(f"${router_cost:.6f}")

        print()

        print("Cost using one model for every prompt:")
        print(f"${baseline_cost:.6f}")

    print()
    print("=" * 70)
    print("TOTAL COST COMPARISON")
    print("=" * 70)

    print()

    print("Cost with cost-aware routing:")
    print(f"${total_router_cost:.6f}")

    print()

    print("Cost using one model for every prompt:")
    print(f"${total_single_model_cost:.6f}")

    savings = total_single_model_cost - total_router_cost

    print()

    print("Estimated savings:")
    print(f"${savings:.6f}")

    if total_single_model_cost > 0:

        savings_percentage = (
            savings / total_single_model_cost
        ) * 100

        print()

        print("Savings percentage:")
        print(f"{savings_percentage:.2f}%")

    print()
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()