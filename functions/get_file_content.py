import os
from config import MAX_CHARS
from google.genai import types

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
    

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Prints the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to print content from, relative to the working directory.",
            ),
        },
    ),
)