import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    valid_dir = os.path.isdir(target_dir)
    
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not valid_dir:
        return f'Error: "{directory}" is not a directory'

    try: 
        target_list = []

        for file_name in os.listdir(target_dir):
            target_path = os.path.join(target_dir, file_name)
            target_size = os.path.getsize(target_path)
            is_target_dir = os.path.isdir(target_path)
            target_list.append(f'- {file_name}: file_size={target_size} bytes, is_dir={is_target_dir}')
            
        return '\n'.join(target_list)

    except Exception as e:
        return f'Error: {e}'

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)