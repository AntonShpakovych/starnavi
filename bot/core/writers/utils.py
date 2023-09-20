import os


def handle_folder_and_file(folder: str, file: str) -> str:
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, file)

    return file_path
