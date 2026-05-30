import os

import requests

MODEL = "google/gemma-4-31b-it:free"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

class Provider:
    def generate(self, messages) -> str:
        api_key = (os.environ.get("OPENROUTER_API_KEY") or "").strip()
        if api_key.lower().startswith("bearer "):
            api_key = api_key[7:].strip()
        api_key = api_key.strip("\"'")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is required")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json={
                "model": MODEL,
                "messages": messages,
            },
            timeout=60,
        )
        if response.status_code >= 400:
            raise RuntimeError(
                f"OpenRouter request failed with {response.status_code}: {response.text}"
            )

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as exc:
            raise RuntimeError(
                f"OpenRouter response did not include message content: {data}"
            ) from exc
