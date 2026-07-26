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


