MODEL_PRICING = {
    "gemini-2.0-flash": {
        "provider": "Google",
        "input_cost_per_1k_tokens": 0.0001,
        "output_cost_per_1k_tokens": 0.0004
    },

    "llama-3.1-8b": {
        "provider": "Groq",
        "input_cost_per_1k_tokens": 0.00005,
        "output_cost_per_1k_tokens": 0.00008
    },

    "command-r": {
        "provider": "Cohere",
        "input_cost_per_1k_tokens": 0.0005,
        "output_cost_per_1k_tokens": 0.0015
    }
}


def get_model_price(model_name):
    return MODEL_PRICING.get(model_name)

def get_cheapest_model():
    cheapest_model = None
    lowest_cost = float("inf")

    for model, details in MODEL_PRICING.items():
        total_cost = (
            details["input_cost_per_1k_tokens"]
            + details["output_cost_per_1k_tokens"]
        )

        if total_cost < lowest_cost:
            lowest_cost = total_cost
            cheapest_model = model

    return cheapest_model

def calculate_cost(model_name, input_tokens, output_tokens):
    model = MODEL_PRICING.get(model_name)

    if model is None:
        return None

    input_cost = (
        input_tokens / 1000
    ) * model["input_cost_per_1k_tokens"]

    output_cost = (
        output_tokens / 1000
    ) * model["output_cost_per_1k_tokens"]

    total_cost = input_cost + output_cost

    return total_cost

def calculate_cost(model_name, input_tokens, output_tokens):
    model = MODEL_PRICING.get(model_name)

    if model is None:
        return None

    input_cost = (
        input_tokens / 1000
    ) * model["input_cost_per_1k_tokens"]

    output_cost = (
        output_tokens / 1000
    ) * model["output_cost_per_1k_tokens"]

    total_cost = input_cost + output_cost

    return round(total_cost, 6)