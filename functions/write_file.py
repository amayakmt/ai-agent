import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    valid_file =  not os.path.isdir(target_file)

    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not valid_file:
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    # make sure that all parent directories of the file_path exist
    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    try:
        with open(target_file, "w") as f:

            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
        
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Enables writing in a new file or overwriting the specified file, putting required arguments: file_path (absolute) and content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative file path to which the user refers to write or overwrite",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The actual content that will be used to write or overwrite the content of 'file_path'. This content will create a new file or replace everything in the specified file"
            )
        },
    ),
)
