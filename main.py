try:
    import openai
except ImportError as e:
    print("Dependency missing. Please run `make install`.")
    exit(str(e))

import os
from modules import BasicLLM
from constants import OLLAMA_ENDPOINT, LMSTUDIO_ENDPOINT, full_config
from helpers import load_env

load_env()

endpoint = OLLAMA_ENDPOINT
if os.environ["PROVIDER"] == "lmstudio":
    endpoint = LMSTUDIO_ENDPOINT


def print_separator() -> None:
    print()
    print("==" * 20)


if __name__ == "__main__":
    client = openai.OpenAI(base_url=endpoint, api_key=os.environ["OPENAI_API"])
    llm = BasicLLM(client)
    while True:
        print_separator()

        prompt = input("User> ")

        print_separator()

        if prompt.lower() == "exit":
            break

        llm.run(command=prompt, **full_config)
