import os
import pathlib
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file in a specified directory relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to python file to be run, relative to the working directory (required)",
            ),"args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A single arugument added to the command line of the file to be run."),
                description="List of arguments to arguments to be used when running the python file (optional)",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    
    timeout = 30

    try:

        abs_working_dir = os.path.abspath(working_directory)
        norm_file_path = os.path.normpath( os.path.join( abs_working_dir, file_path))
        
        if not os.path.commonpath([abs_working_dir, norm_file_path]) == abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(norm_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if pathlib.Path(norm_file_path).suffix != '.py':
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", norm_file_path]
        if args is not None:
            command.extend(args)
        
        subprocess_return = subprocess.run(command, cwd=abs_working_dir, text=True, capture_output=True, timeout=timeout)

        subprocess_output = f"####### Running {norm_file_path} #######\n"

        if subprocess_return.returncode != 0:
            subprocess_output += f"Process exited with code {subprocess_return.returncode}" + "\n"
        
        if len(subprocess_return.stdout) < 1 and len(subprocess_return.stderr) < 1:
            subprocess_output += f"No output produced" + "\n"
        else:
            if len(subprocess_return.stdout) > 0:
                subprocess_output += f"STDOUT: {subprocess_return.stdout} \n"
            if len(subprocess_return.stderr) > 0:
                subprocess_output += f"STDERR: {subprocess_return.stderr} \n"
        return str(subprocess_output)
                

    except Exception as e:
        return f"Error: executing Python file: {e}"

        

