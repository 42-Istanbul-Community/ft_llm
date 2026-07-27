try:
    import openai
except ImportError as e:
    print(e)

try:
    import jinja2
except ImportError as e:
    print(e)
else:
    print("Ready to roll!")


from modules.llm import BasicLLM
from helpers.utils import get_jinja2


client = openai.OpenAI()
llm = BasicLLM(client)
llm.respond("Hey")
