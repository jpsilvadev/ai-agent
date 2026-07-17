import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abspath = os.path.abspath(working_directory)
        abs_filepath = os.path.normpath(os.path.join(working_dir_abspath, file_path))

        valid_target_dir = (
            os.path.commonpath([working_dir_abspath, abs_filepath])
            == working_dir_abspath
        )
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_filepath):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_filepath]
        if args:
            command.extend(args)
        process = subprocess.run(
            command,
            cwd=working_dir_abspath,
            capture_output=True,
            check=False,
            text=True,
            timeout=30,
        )

        process_output = []
        if process.returncode != 0:
            return f"Process exited with code {process.returncode}"

        if not process.stdout and not process.stderr:
            process_output.append("No output produced")
        else:
            process_output.append(f"STDOUT: {process.stdout}")
            process_output.append(f"STDERR: {process.stderr}")

        return "\n".join(process_output)
    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified python file relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "descrption": "Optional args to pass to python file execution",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}
