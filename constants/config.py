from openai._types import NOT_GIVEN

full_config = {
    "name": "empty",
    "channel_id": None,
    # "model": "",
    "temperature": 0.0,  # Min 0, Max 3
    "top_p": 0.96,
    "presence_penalty": 0,  # min -2, max 2
    "frequency_penalty": 0,  # min -2, max 2
    "stream": True,
    "top_k": 40,
    "min_p": 0.5
}
