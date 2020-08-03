import os.path
import subprocess
import sys

PRIVILEGED_DIR = "./privileged_scripts"


def run_privileged(script_name: str, *args: str, **kwargs):
    python_interpreter = sys.executable
    subprocess.run(
        ["sudo", python_interpreter, os.path.join(PRIVILEGED_DIR, script_name), *args],
        **kwargs,
        check=True
    )
