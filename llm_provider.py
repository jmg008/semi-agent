import subprocess

class Provider:
    def generate(self, message: str) -> str:
        result = subprocess.run(
            ["codex", "exec", message],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()