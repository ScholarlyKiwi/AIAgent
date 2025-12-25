import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["directory"],
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    file_output = f"Result for '{directory}' directory:\n"

    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath( os.path.join(abs_working_dir, directory) )
        valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
        target_dir_exists = os.path.exists(target_dir)
    except Exception as e:
        file_output += f"Error: Error in target directory: {e}"
    else:
        if not valid_target_dir:
            file_output += f'Error: Cannot list "{target_dir}" as it is outside the permitted working directory'
        elif not target_dir_exists:
            file_output += f'Error: "{target_dir}" is not a directory'
        else:
            try:
                file_info = list()
                for dir_obj in os.listdir(target_dir):
                    file_path = os.path.join(target_dir, dir_obj)
                    is_dir = os.path.isdir(file_path)
                    file_size = os.path.getsize(file_path)

                    file_info.append(f"  - {dir_obj}: file_size={file_size} bytes, is_dir={is_dir}")

                file_output += '\n'.join(file_info)

            except Exception as e:
                file_output += f'Error: unable to process contents: {e}'

    return file_output

