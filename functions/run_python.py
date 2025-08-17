import os
import subprocess
import sys


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
    
