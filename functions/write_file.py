import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abspath = os.path.abspath(working_directory)
        abs_filepath = os.path.normpath(os.path.join(working_dir_abspath, file_path))

        valid_target_dir = (
            os.path.commonpath([working_dir_abspath, abs_filepath])
            == working_dir_abspath
        )
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(abs_filepath):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(abs_filepath)
        os.makedirs(parent_dir, exist_ok=True)
        with open(abs_filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"
