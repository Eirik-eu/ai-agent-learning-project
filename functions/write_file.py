import os
from google.genai import types

def write_file(working_directory, file_path, content):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_dir = os.path.abspath(working_directory)

    if not full_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(full_path) and os.path.isdir(full_path):
        return f'Error: "{file_path}" is a directory, not a file'
    
    try:
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing to file: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that should be written to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that should be written to the file.",
            ),
        },
    ),
)