try:
    import openai
except ImportError as e:
    print("Dependency missing. Please run `make install`.")
    print(e)

import os
from modules import BasicLLM
from constants import OLLAMA_ENDPOINT, LMSTUDIO_ENDPOINT, full_config
from helpers import load_env

load_env()

endpoint = OLLAMA_ENDPOINT
if os.environ["PROVIDER"] == "lmstudio":
    endpoint = LMSTUDIO_ENDPOINT


def print_seperator() -> None:
    print()
    print("=="*20)


if __name__ == "__main__":
    client = openai.OpenAI(base_url=endpoint, api_key=os.environ["OPENAI_API"])
    llm = BasicLLM(client)
    while True:
        print_seperator()

        prompt = input("User> ")

        print_seperator()

        if prompt.lower() == "exit":
            break

        llm.run(command=prompt, **full_config)
