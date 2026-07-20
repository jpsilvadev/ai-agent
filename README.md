# ai-agent

A command-line AI coding agent. It sends your prompt to an LLM (via OpenRouter) and lets the model call local tools to explore and modify a working directory: listing files, reading file contents, running Python files, and writing files.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)
- An [OpenRouter](https://openrouter.ai/) API key

## Setup

Install dependencies:

```bash
uv sync
```

Create a `.env` file in the project root with your API key:

```env
OPENROUTER_API_KEY=your-key-here
```

## Usage

Run the agent with a prompt:

```bash
uv run main.py "your prompt here"
```

Add `--verbose` to see token usage and tool call output:

```bash
uv run main.py "your prompt here" --verbose
```

The agent operates on the directory set as `WORKING_DIRECTORY` in `config.py` (defaults to `./calculator`). It loops until it produces a final response or hits `MAX_ITERATIONS`, both configurable in `config.py`.

## Project structure

```text
.
├── main.py            # entry point, CLI args, agent loop
├── prompts.py         # system prompt
├── config.py          # iteration limit, char limit, working directory
├── call_function.py   # dispatches tool calls to functions
├── functions/         # tool implementations (file listing, reading, writing, running Python)
└── calculator/        # sandbox project used to exercise the agent, not part of the agent itself
```
