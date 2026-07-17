import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abspath = os.path.abspath(working_directory)
        abs_filepath = os.path.normpath(os.path.join(working_dir_abspath, file_path))

        valid_target_dir = (
            os.path.commonpath([working_dir_abspath, abs_filepath])
            == working_dir_abspath
        )
        if not valid_target_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_filepath):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_filepath, "r", encoding="utf-8") as f:
            # read only up to MAX_CHARS to prevent burning too many tokens when sending to LLM
            content = f.read(MAX_CHARS)

            # if content still exists we reached MAX_CHARS
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

            return content
    except Exception as e:
        return f"Error: {e}"
