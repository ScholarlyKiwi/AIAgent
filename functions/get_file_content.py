import os
from config import MAX_CHARS

from google.genai import types

schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the text with a specific file, truncated at the configured max characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the file whoose text will be returned. The file path is relative to the working directory (required)",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):

    try:
        abs_working_dir = os.path.abspath(working_directory)
        norm_file_path = os.path.normpath( os.path.join( abs_working_dir, file_path))
        valid_target_file = os.path.commonpath([abs_working_dir, norm_file_path]) == abs_working_dir


        if not valid_target_file:
            return f'Error: Cannot read "{norm_file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(norm_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        open_file = open(norm_file_path)
        content = open_file.read(MAX_CHARS)

        # After reading the first MAX_CHARS...
        if open_file.read(1):
            content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        open_file.close()

        return content

    except Exception as e:
        return f"Error: Error in target directory: {e}"
