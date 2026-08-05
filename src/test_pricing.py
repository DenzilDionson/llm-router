from pricing import (
    get_model_price,
    get_cheapest_model,
    calculate_cost
)


price = get_model_price("gemini-2.0-flash")

print("Gemini price:")
print(price)


cheapest = get_cheapest_model()

print("\nCheapest model:")
print(cheapest)


cost = calculate_cost(
    "gemini-2.0-flash",
    2000,
    1000
)

print("\nRequest cost:")
print(cost)