import os
import hashlib
import zipfile

from tig_common import *

def tig_add(files):
    for file in files:
        if not os.path.exists(file):
            print("file: " + file + " not exist")
            return
        if os.path.isdir(file):
            print(file + " is a directory, please input a file path")
            return

        md5 = calculate_md5(file)
        compress_file_path = os.path.join(tig_objects_directory(), md5)
        if os.path.exists(compress_file_path):
            return
        compress_files(file, compress_file_path)
        update_index(file, md5)

def calculate_md5(filename):
    with open(filename, 'rb') as file:
        md5_hash = hashlib.md5()
        while chunk := file.read(4096):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def compress_files(file, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file)

def update_index(file, md5):
    rel_path = os.path.relpath(file, project_directory())
    data = read_uncommited_files()
    data[rel_path] = md5
    save_uncommited_files(data)