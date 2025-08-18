import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_dir = os.path.abspath(working_directory)

    if not full_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    if not full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(["python", full_path, *args], timeout=5, capture_output=True, text=True, cwd=abs_working_dir)
        if result.returncode != 0:
            return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}. Process exited with code {result.returncode}"
        if result.stdout == "":
            return "No output produced."
        return f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file with it's relevant arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file that should be executed, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Optional arguments that should be passsed to the python file if relevant.",
            ),
        },
    ),
)