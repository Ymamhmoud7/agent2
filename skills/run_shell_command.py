import subprocess
import shlex

DESCRIPTION = "Run any shell command and return its output."

EXAMPLES = [
    {
        "user": "run ls -la in my home directory",
        "plan": [
            {
                "type": "call",
                "function": "run_shell_command",
                "args": {
                    "command": "ls -la ~"
                }
            }
        ]
    },
    {
        "user": "what's my current IP address?",
        "plan": [
            {
                "type": "call",
                "function": "run_shell_command",
                "args": {
                    "command": "curl -s ifconfig.me"
                }
            }
        ]
    }
]




def run_shell_command(command: str, timeout: int = 30, working_dir: str = None) -> dict:
    """
    Run a shell command and return its output.

    Args:
        command:     The shell command to execute (e.g. "ls -la ~/documents").
        timeout:     Maximum seconds to wait before killing the process. Defaults to 30.
        working_dir: Directory to run the command in. Defaults to current directory.

    Returns:
        dict with keys: success (bool), command (str), stdout (str), stderr (str),
                        exit_code (int|None), message (str)
    """
    if not command or not command.strip():
        return {"success": False, "command": command, "stdout": "", "stderr": "", "exit_code": None, "message": "Command cannot be empty."}

    command = command.strip()

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=working_dir
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        success = result.returncode == 0
        message = f"Command exited with code {result.returncode}."
        if not success and stderr:
            message = f"Command failed (exit {result.returncode}): {stderr}"
        return {
            "success": success,
            "command": command,
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": result.returncode,
            "message": message
        }
    except FileNotFoundError:
        return {"success": False, "command": command, "stdout": "", "stderr": "", "exit_code": None, "message": f"Working directory '{working_dir}' does not exist."}
    except subprocess.TimeoutExpired:
        return {"success": False, "command": command, "stdout": "", "stderr": "", "exit_code": None, "message": f"Command timed out after {timeout} seconds."}
    except Exception as e:
        return {"success": False, "command": command, "stdout": "", "stderr": "", "exit_code": None, "message": f"Unexpected error: {e}"}