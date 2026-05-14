import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    valid_working_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    valid_file = os.path.isfile(target_file)

    if not valid_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not valid_file:
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    # Subprocess Command Execution
    try: 
        command = ["python", target_file]
        if args:
            command.extend(args)
        
        result = subprocess.run(command, capture_output=True, timeout=30, text=True)

        output = ""
        
        if result.returncode != 0:
            output += f'Process exited with code {result.returncode}\n'
        if not result.stderr and not result.stdout:
            output += f'No output produced\n'
        
        output += f'STDOUT: {result.stdout}\n'
        output += f'STDERR: {result.stderr}\n'

        return output

    except Exception as e:
        return f'Error: executing Python file: {e}'    

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specific Python file, giving 2 arguments: absolute Python file path (file_path) and (optionally) arguments as a list",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative file path to a specified Python file that a user wishes to execute",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description= "Some Python files require additional arguments (e.g. calculator.py -> ['3 + 5']. These can be passed as 'args=[]')"
            )
        },
    ),
)