import os

def delete_folder(folder_path):
    """
    Deletes the specified folder and all its contents.

    Args:
        folder_path (str): The path to the folder to be deleted.
    """
    if os.path.exists(folder_path):
        try:
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(folder_path)
            return f"Folder '{folder_path}' has been deleted successfully."
        except Exception as e:
            return f"An error occurred while deleting the folder: {e}"
    else:
        return f"The folder '{folder_path}' does not exist."