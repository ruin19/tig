import os
import zipfile
from tig_tree import *

from tig_common import *

def tig_add(paths):
    tree = Tree()
    tree.load_commit_tree()
    # 已提交的 文件 - md5 映射
    commit_file_paths = tree.file_paths()

    # 暂存区的 文件 - md5 映射
    uncommited_files = read_uncommited_files()

    project_dir = project_directory()

    add_or_modify_files = []
    delete_files = []
    # TODO 删除暂时只支持指定具体文件，不支持按 . 通配
    for path in paths:
        if path == ".":
            path = os.getcwd()
        if not os.path.exists(path):
            path_rel_project = os.path.relpath(os.path.join(os.getcwd(), path), project_dir)
            if not path_rel_project in commit_file_paths and not path_rel_project in uncommited_files:
                print("fatal: pathspec \'" + path + "\' did not match any files")
                exit(1)
            delete_files.append(path_rel_project)
            continue
        if os.path.isdir(path):
            files_in_dir = local_files_in_directory(path)
            for f in files_in_dir:
                f_rel_current = os.path.relpath(os.path.join(project_dir, f), os.getcwd())
                add_or_modify_files.append(f_rel_current)
        else:
            add_or_modify_files.append(path)

    for file in add_or_modify_files:
        file_rel_project = os.path.relpath(file, project_dir)
        md5 = file_md5(file)
        compress_file_path = os.path.join(tig_objects_directory(), md5)
        if os.path.exists(compress_file_path):
            if file_rel_project in commit_file_paths and commit_file_paths[file_rel_project] == md5:
                continue
        else:
            compress_files(file, compress_file_path)
        update_index(file, md5)
    
    for file in delete_files:
        update_index(file, "")


def compress_files(file, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file)

def update_index(file, md5):
    rel_path = os.path.relpath(file, project_directory())
    data = read_uncommited_files()
    data[rel_path] = md5
    save_uncommited_files(data)