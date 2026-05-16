import os

def create_folder(folder_name):
    """Create a new folder with the given name."""
    os.makedirs(folder_name, exist_ok=True)
    return f"Folder '{folder_name}' created successfully."