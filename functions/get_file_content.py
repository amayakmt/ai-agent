import os
import sys
sys.path.append("..")
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    valid_file = os.path.isfile(target_file)

    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not valid_file:
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(target_file) as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content

    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Provides contents of a file in a specified file_path using its absolute file path, giving the output of up to 10,000 characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative file path to which the user refers to get its contents",
            ),
        },
    ),
)
