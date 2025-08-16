import os

def get_files_info(working_directory, directory="."):
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    abs_working_dir = os.path.abspath(working_directory)
    if not full_path.startswith(abs_working_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
        
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory\n'

    try:
        dir_contents = os.listdir(full_path)
        return_string = ""
        for content in dir_contents:
            content_path = os.path.join(full_path, content)
            return_string += f"- {content}: file_size={os.path.getsize(content_path)} bytes, is_dir={os.path.isdir(content_path)}\n"

        return return_string
    except Exception as e:
        return f"Error listing files: {e}"


