# semi-agent

`semi-agent`는 LLM 기반 코딩 에이전트의 가장 작은 동작 단위를 실험하는 프로젝트입니다.

모델이 사용자 요청을 해석하고, 필요한 작업을 JSON 형식으로 표현한 뒤, 로컬 터미널 도구를 호출해 `target_project` 안에서 명령을 실행합니다. 직접 파일을 수정하는 거대한 에이전트 프레임워크가 아니라, "모델의 판단", "도구 호출", "결과 피드백"이라는 기본 흐름을 단순한 코드로 확인하는 데 초점을 둡니다.

## 프로젝트 목표

- LLM 응답을 구조화된 JSON 프로토콜로 제한합니다.
- 에이전트가 도구 호출과 최종 응답을 구분해 처리합니다.
- 터미널 실행 결과를 다시 모델에게 전달해 다음 행동을 결정하게 합니다.
- 복잡한 프레임워크 없이 코딩 에이전트의 핵심 루프를 이해할 수 있게 합니다.

## 동작 방식

1. `main.py`에서 작업 내용을 정해 `Agent`를 실행합니다.
2. `Agent`는 시스템 프롬프트와 사용자 작업을 OpenRouter 모델에 전달합니다.
3. 모델은 JSON으로 다음 행동을 응답합니다.
4. 응답 타입이 `tool_call`이면 `tools.py`의 터미널 도구를 실행합니다.
5. 실행 결과를 다시 대화 기록에 넣고 모델에게 다음 단계를 요청합니다.
6. 응답 타입이 `final`이면 작업을 종료합니다.

## 주요 구성

```text
.
|-- agent.py          # 에이전트 루프, JSON 파싱, 도구 호출 처리
|-- llm_provider.py   # OpenRouter API 요청 처리
|-- main.py           # 예시 작업 실행 진입점
|-- tools.py          # target_project 기준 터미널 도구
|-- requirements.txt  # Python 의존성
`-- README.md
```

## 실행 준비

Python 의존성을 설치합니다.

```bash
pip install -r requirements.txt
```

OpenRouter API 키를 환경변수로 설정합니다.

```bash
# PowerShell
$env:OPENROUTER_API_KEY = "your-openrouter-api-key"

# macOS/Linux
export OPENROUTER_API_KEY="your-openrouter-api-key"
```

에이전트가 작업할 폴더를 만듭니다.

```bash
mkdir target_project
```

## 실행

```bash
python main.py
```

작업 내용은 `main.py`의 `task` 값을 수정해 바꿀 수 있습니다.

```python
from agent import Agent

task = "src/text_utils.py 파일을 만들고 Hello, World!를 출력하는 코드를 작성해줘"

agent = Agent(task)
agent.run()
```

## JSON 응답 프로토콜

모델은 매 단계에서 하나의 JSON 객체만 반환해야 합니다.

도구 호출 예시:

```json
{
  "message": "먼저 파일 목록을 확인하겠습니다.",
  "type": "tool_call",
  "tool": "terminal",
  "args": {
    "command": "dir"
  }
}
```

작업 종료 예시:

```json
{
  "message": "작업을 완료했습니다.",
  "type": "final",
  "answer": "src/text_utils.py 파일을 생성했습니다."
}
```

## 현재 범위

- 사용 가능한 도구는 `terminal` 하나입니다.
- 터미널 명령은 `target_project` 폴더 안에서 실행됩니다.
- 모델이 JSON이 아닌 응답을 반환하면 에이전트는 오류를 발생시킵니다.
- `tools.py`는 `shell=True`로 명령을 실행하므로 신뢰할 수 있는 작업에만 사용해야 합니다.

## 모델 설정

기본 모델은 `llm_provider.py`에 정의되어 있습니다.

```python
MODEL = "google/gemma-4-31b-it:free"
```

다른 OpenRouter 모델을 사용하려면 이 값을 변경하면 됩니다.
