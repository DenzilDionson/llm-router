from src.llm_client import call_llm

if __name__ == "__main__":
    result = call_llm("Say hello in one word.", provider="groq")
    print(result)