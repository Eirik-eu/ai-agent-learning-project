import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_dir = os.path.abspath(working_directory)

    if not full_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory\n'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"\n'

    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

        return f'{file_content_string}[...File "{file_path}" truncated at 10000 characters]'
    except Exception as e:
        return f"Error listing files: {e}"