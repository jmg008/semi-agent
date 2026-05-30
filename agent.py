import json

from llm_provider import Provider
from tools import TOOLS

SYSTEM_PROMPT = """너는 터미널 도구를 사용할 수 있는 코딩 에이전트다.

너는 직접 파일을 보거나 수정할 수 없다.
대신 terminal 도구를 호출하여 명령을 실행할 수 있다.

사용 가능한 도구:

1. terminal
   - 설명: target_project 폴더 안에서 터미널 명령을 실행한다.
   - args: {"command": "실행할 명령"}
   - 실행 환경: Window

매 응답은 반드시 JSON 하나여야 한다.
마크다운, 코드블록, JSON 밖의 설명은 쓰지 마라.

응답에는 항상 message 필드를 포함하라.
message에는 사용자에게 보여줄 짧은 진행 설명을 한 문장으로 적어라.
내부 추론 과정을 길게 쓰지 말고, 지금 무엇을 하려는지만 말하라.

도구를 사용할 때:
{
  "message": "먼저 파일 목록을 확인하겠습니다.",
  "type": "tool_call",
  "tool": "terminal",
  "args": {
    "command": "dir"
  }
}

작업을 완료했을 때:
{
  "message": "모든 테스트가 통과했으므로 작업을 마무리하겠습니다.",
  "type": "final",
  "answer": "최종 답변"
}
"""

class Agent:
    def __init__(self, task):
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task},
        ]
        self.provider = Provider()

    def parse_response(self, response):
        try:
            return json.loads(response)
        except json.JSONDecodeError as exc:
            print(response)
            raise ValueError("Provider response is not valid JSON") from exc

    def call_tool(self, tool_name, arg):

    def run(self):