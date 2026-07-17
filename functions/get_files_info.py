import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abspath = os.path.abspath(working_directory)
        abs_filepath = os.path.normpath(os.path.join(working_dir_abspath, directory))

        valid_target_dir = (
            os.path.commonpath([working_dir_abspath, abs_filepath])
            == working_dir_abspath
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_filepath):
            return f'Error: "{abs_filepath}" is not a directory'

    except Exception as e:
        return f"Error: {e}"

    try:
        directory_repr = ""
        for item in os.listdir(abs_filepath):
            # skip __pycache__ or similars
            if item.startswith("__"):
                continue

            path = os.path.normpath(os.path.join(abs_filepath, item))
            path_size = os.path.getsize(path)
            is_dir = os.path.isdir(path)

            directory_repr += (
                f"- {item}: file_size={path_size} bytes, is_dir={is_dir}\n"
            )
        return directory_repr
    except Exception as e:
        return f"Error: {e}"
