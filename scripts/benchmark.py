"""
Benchmark logging script for the LLM Router.

Measures:
- Model used
- Latency
- Input tokens
- Output tokens
- Cost
- Success/failure
"""

import json
import time

from src.llm_client import call_llm


def run_benchmark(prompt: str, provider: str = "groq"):
    """
    Run a prompt through the shared LLM client
    and collect benchmark metrics.
    """

    start_time = time.time()

    try:
        result = call_llm(prompt, provider=provider)

        latency = time.time() - start_time

        benchmark_result = {
            "prompt": prompt,
            "provider": result["provider"],
            "model": result["model"],
            "latency_seconds": round(latency, 4),
            "input_tokens": result["tokens_in"],
            "output_tokens": result["tokens_out"],
            "cost": result["cost"],
            "status": "success",
            "response": result["text"],
        }

    except Exception as error:

        latency = time.time() - start_time

        benchmark_result = {
            "prompt": prompt,
            "provider": provider,
            "model": None,
            "latency_seconds": round(latency, 4),
            "input_tokens": None,
            "output_tokens": None,
            "cost": None,
            "status": "failed",
            "error": str(error),
        }

    return benchmark_result


def main():
    """Run the benchmark using a sample prompt."""

    prompt = "Explain what artificial intelligence is in one sentence."

    result = run_benchmark(prompt)

    print("\nBenchmark Result")
    print("----------------")

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()