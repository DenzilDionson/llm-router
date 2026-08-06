from cost_logger import (
    estimate_cost,
    actual_cost,
    log_cost,
)

model = "gemini-2.0-flash"

estimated = estimate_cost(
    model,
    input_tokens=500,
    estimated_output_tokens=400,
)

actual = actual_cost(
    model,
    input_tokens=500,
    output_tokens=470,
)

log_cost(
    model,
    estimated,
    actual,
)