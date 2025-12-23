import os

def write_file(working_directory, file_path, content):
    try:

        abs_working_dir = os.path.abspath(working_directory)
        norm_file_path = os.path.normpath( os.path.join( abs_working_dir, file_path))
        valid_target_file = os.path.commonpath([abs_working_dir, norm_file_path]) == abs_working_dir
        

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
               
        if os.path.isdir(norm_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        directory_path = os.path.dirname(norm_file_path)
        os.makedirs(directory_path, exist_ok=True)
        file_to_write = open(norm_file_path,'w')
        file_to_write.write(content)
        file_to_write.close()

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e: 
        raise Exception(f"Error: Unable to write file {file_path}: {e}")
    return "What?"
