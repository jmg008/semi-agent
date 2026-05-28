import subprocess
from pathlib import Path

WORKSPACE = Path("target_project").resolve()

def run_terminal(command: str):
    result = subprocess.run(
        command,
        shell=True,
        cwd=WORKSPACE,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


TOOLS = {
    "terminal": lambda args: run_terminal(args["command"]),
}