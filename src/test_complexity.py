from complexity import score_prompt, classify_prompt

prompts = [
    "What is Python?",
    "Compare Python and Java with examples.",
    "Build a complete Flask REST API using Docker and PostgreSQL. Explain every step."
]

for prompt in prompts:
    print("-" * 60)
    print("Prompt:")
    print(prompt)
    print()

    print("Score:")
    print(score_prompt(prompt))
    print()

    print("Classification:")
    print(classify_prompt(prompt))
    print()