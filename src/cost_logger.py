from pricing import get_model_price


def estimate_cost(model_name, input_tokens, estimated_output_tokens):
    """
    Estimate the expected API cost before making the request.
    """

    pricing = get_model_price(model_name)

    if pricing is None:
        raise ValueError(f"Unknown model: {model_name}")

    input_cost = (
        input_tokens / 1000
    ) * pricing["input_cost_per_1k_tokens"]

    output_cost = (
        estimated_output_tokens / 1000
    ) * pricing["output_cost_per_1k_tokens"]

    total = input_cost + output_cost

    return round(total, 6)


def actual_cost(model_name, input_tokens, output_tokens):
    """
    Calculate the actual API cost after receiving the response.
    """

    pricing = get_model_price(model_name)

    if pricing is None:
        raise ValueError(f"Unknown model: {model_name}")

    input_cost = (
        input_tokens / 1000
    ) * pricing["input_cost_per_1k_tokens"]

    output_cost = (
        output_tokens / 1000
    ) * pricing["output_cost_per_1k_tokens"]

    total = input_cost + output_cost

    return round(total, 6)


def log_cost(model_name, estimated_cost, actual_cost_value):
    """
    Print cost information.
    """

    print("=" * 60)

    print("Model:")
    print(model_name)

    print()

    print("Estimated Cost:")
    print(f"${estimated_cost}")

    print()

    print("Actual Cost:")
    print(f"${actual_cost_value}")

    print()

    print("Difference:")
    print(f"${round(actual_cost_value-estimated_cost,6)}")

    print("=" * 60)