import json

from llm_provider import Provider
from tools import TOOLS

SYSTEM_PROMPT = ""

class Agent:
    def __init__(self, task):
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task},
        ]
        self.provider = Provider()

    def parse_response(self, response):
        return json.loads(response)

    def call_tool(self, tool_name, arg):
        if tool_name not in TOOLS:
            raise ValueError(f"Unknown tool: {tool_name}")
        return TOOLS[tool_name](arg)

    def run(self):
        while True:
            response = self.provider.generate(
                json.dumps(self.messages, ensure_ascii=False)
            )
            parsed = self.parse_response(response)

            self.messages.append({"role": "assistant", "content": response})
            print(parsed["message"])

            if parsed["type"] == "tool_call":
                tool_name = parsed["tool_name"]
                print(parsed["arg"])
                result = self.call_tool(tool_name, parsed["arg"])
                self.messages.append(
                    {
                        "role": "tool",
                        "name": tool_name,
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )
                continue

            if parsed["type"] == "final":
                return parsed.get("content", parsed["message"])

            raise ValueError(f"Unknown response type: {parsed['type']}")
