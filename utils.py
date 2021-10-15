import os


def check_file_exists(filepath):
    return os.path.isfile(filepath)


def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    return content
