from router import select_model

prompts = [
    "What is Python?",
    "Compare Python and Java.",
    "Build a complete REST API using Flask, Docker and PostgreSQL."
]

for prompt in prompts:

    print("-" * 60)

    print("Prompt:")
    print(prompt)

    print()

    print("Selected model:")

    print(select_model(prompt))

    print()