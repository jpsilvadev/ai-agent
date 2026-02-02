import os


def get_files_info(working_directory, directory="."):
    abs_path = os.path.abspath(working_directory)
    fpath = os.path.normpath(os.path.join(abs_path, directory))
    valid_path = os.path.commonpath([abs_path, fpath]) == abs_path

    if not valid_path:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # TODO:
