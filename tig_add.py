import os
import zipfile
from tig_tree import *

from tig_common import *

def tig_add(paths):
    files = []
    for path in paths:
        if path == ".":
            path = os.getcwd()
        if not os.path.exists(path):
            print("path: " + path + " not exist")
            continue
        if os.path.isdir(path):
            files_in_dir = local_files_in_directory(path)
            files.extend(files_in_dir)
        else:
            files.append(path)

    tree = Tree()
    tree.load_commit_tree()
    # 已提交的 文件 - md5 映射
    commit_file_paths = tree.file_paths()

    for file in files:
        md5 = file_md5(file)
        compress_file_path = os.path.join(tig_objects_directory(), md5)
        if os.path.exists(compress_file_path):
            if file in commit_file_paths and commit_file_paths[file] == md5:
                continue
        else:
            compress_files(file, compress_file_path)
        update_index(file, md5)

def compress_files(file, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file)

def update_index(file, md5):
    rel_path = os.path.relpath(file, project_directory())
    data = read_uncommited_files()
    data[rel_path] = md5
    save_uncommited_files(data)