import os

def read_file(file_path):
    """Reads the content of a file and returns it as a string."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    return content

def save_file(file_path, content):
    """Saves the given content to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def get_file_extension(file_path):
    """Returns the file extension of the given file path."""
    return os.path.splitext(file_path)[1]