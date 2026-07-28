try:
    import openai
except ImportError as e:
    print("Dependency missing. Please use `make install`.")
    print(e)
else:
    print("Ready to roll!")

import os
from modules import BasicLLM
from constants import OLLAMA_ENDPOINT, LMSTUDIO_ENDPOINT
from helpers import load_env

load_env()

endpoint = OLLAMA_ENDPOINT

if os.environ["PROVIDER"] == "lmstudio":
    endpoint = LMSTUDIO_ENDPOINT

client = openai.OpenAI(base_url=endpoint, api_key=os.environ["OPENAI_API"])
llm = BasicLLM(client)

while True:
    prompt = input("User> ")
    if prompt.lower() == "exit":
        break
    llm.respond(message=prompt)
