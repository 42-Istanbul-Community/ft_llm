_A growing repository for local LLM inference with minimal dependencies maintained by aozsen._

# School42 Local AI Chat Interface 🎓💻

**Purpose:** Minimal codebase demonstrating how to interact with local Large Language Models using Ollama and the OpenAI API. Designed for collaborative learning by students at **School 42**. This project intentionally keeps dependencies low so new contributors can run it on any machine or container without complex setup.

## Prerequisites
1. A Linux environment (Ubuntu) — typical of our labs
2. python >= 3.13.5

### Install Dependencies
```bash 
make install
```

## Usage
```bash 
make run # creates virtual environment (.venv) and installs dependencies if necessary.
```

### Slash commands

- `/ct <float>`: Change temperature
- `/ca <string>`: Change ai(persona)
- `/cpp <float>`: Set presence_penalty (-2 / 2)
- `/cfp <float>`: Set frequency_penalty (-2 / 2)
- `/save <string>`: Save the current conversation
- `/load <string>`: Load a previously saved conversation
- `/rev <int>`: Revert 'x' messages back


## Contributing Guidelines 🤝  

This project lives at School 42, where peer-to-peer teaching and code sharing are core values. Before contributing:
1. Fork this repository first using GitHub's [Fork & Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests) flow  
2. Follow the `.gitignore` rules — never commit secrets or local env files (`.env`) to main branch

If you want to add new functionality, write a clear PR title describing what changes do and why they help other students learn more efficiently.
