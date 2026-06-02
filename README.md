# semi-agent

`semi-agent` is a minimal coding agent prototype. It sends a task to an
OpenRouter-hosted language model, asks the model to respond with structured
JSON, and lets the model run terminal commands inside a `target_project`
workspace through a single local tool.

## Features

- OpenRouter chat-completions integration
- JSON-only agent response protocol
- Terminal tool execution scoped to `target_project`
- Iterative agent loop with tool-call and final-answer handling

## Project Structure

```text
.
|-- agent.py          # Agent loop, response parsing, and tool dispatch
|-- llm_provider.py   # OpenRouter API client
|-- main.py           # Example entry point with a sample task
|-- tools.py          # Local terminal tool implementation
|-- requirements.txt  # Python dependencies
`-- README.md
```

## Requirements

- Python 3.10 or later
- An OpenRouter API key

Install dependencies:

```bash
pip install -r requirements.txt
```

Set the OpenRouter API key:

```bash
# PowerShell
$env:OPENROUTER_API_KEY = "your-openrouter-api-key"

# macOS/Linux
export OPENROUTER_API_KEY="your-openrouter-api-key"
```

## Usage

Create a `target_project` directory in the repository root. The terminal tool
runs commands from that directory.

```bash
mkdir target_project
python main.py
```

`main.py` currently contains a hard-coded sample task. Edit the `task` value to
change what the agent should attempt:

```python
from agent import Agent

task = "Create src/text_utils.py and add code that prints Hello, World!"

agent = Agent(task)
agent.run()
```

## Agent Protocol

The model is expected to return exactly one JSON object per step.

Tool call:

```json
{
  "message": "I will inspect the project files first.",
  "type": "tool_call",
  "tool": "terminal",
  "args": {
    "command": "dir"
  }
}
```

Final response:

```json
{
  "message": "The task is complete.",
  "type": "final",
  "answer": "Created src/text_utils.py."
}
```

## Configuration

The default model is configured in `llm_provider.py`:

```python
MODEL = "google/gemma-4-31b-it:free"
```

Change this value if you want to use a different OpenRouter model.

## Limitations

- The only available tool is `terminal`.
- Tool commands are executed with `shell=True`, so only run this against
  projects and tasks you trust.
- The agent does not currently modify files directly outside shell commands.
- `target_project` must exist before running the example.
- If the model returns non-JSON output, the agent raises an error.

## Troubleshooting

- `OPENROUTER_API_KEY is required`: set the `OPENROUTER_API_KEY` environment
  variable before running the agent.
- `OpenRouter request failed`: check the API key, model availability, and
  network connection.
- `Provider response is not valid JSON`: the model did not follow the required
  JSON response format. Try a more instruction-following model or tighten the
  system prompt.
