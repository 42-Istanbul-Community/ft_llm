full_config = {
    "name": "default",
    "model": "orn:latest",
    "temperature": 0.0,  # Min 0, Max 3
    "top_p": 0.96,
    "presence_penalty": 0.0,  # min -2, max 2
    "frequency_penalty": 0.0,  # min -2, max 2
    "stream": True,
    "top_k": 40,  # invalid for openai client
    "min_p": 0.5  # invalid for openai client
}

LMSTUDIO_ENDPOINT = "http://127.0.0.1:1234/v1"
OLLAMA_ENDPOINT = "http://127.0.0.1:11434/v1"
