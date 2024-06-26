import os
from tig_common import *
from tig_tree import *

def tig_status():
    commited_files, uncommited_files, modified_files, untracked_files, deleted_files = fetch_status()

    # 打印暂存区文件
    if uncommited_files:
        print("Changes to be committed:")
        for file in uncommited_files.keys():
            if file in commited_files:
                if uncommited_files[file]:
                    print(GREEN + "\tmodified:\t" + file + END)
                else:
                    print(GREEN + "\tdeleted:\t" + file + END)

            else:
                print(GREEN + "\tnew file\t" + file + END)

    # 打印修改后未提交暂存区的文件
    if modified_files or deleted_files:
        print("Changes not staged for commit:")

        for file in deleted_files:
            print(RED + "\t" + "deleted:\t" + file + END)

        for file in modified_files:
            print(RED + "\t" + "modified:\t" + file + END)


    # 打印新增的未提交暂存区的文件
    if untracked_files:
        print("Untracked files:")
        for file in untracked_files:
            print(RED + "\t" + file + END)

def fetch_status():
    tree = Tree()
    tree.load_commit_tree()
    # 已提交的 文件 - md5 映射
    committed_files = tree.file_paths()

    # 暂存区的 文件 - md5 映射
    uncommited_files = read_uncommited_files()

    # 本地文件数组
    local_file_paths = set(local_files())

    project_dir = project_directory()

    modified_files = []
    untracked_files = []

    # 遍历本地文件，看是否已在版本库，是否在暂存区，以及md5是否跟版本库或暂存区相同来判断处于什么状态
    for file in local_file_paths:
        local_md5 = file_md5(os.path.join(project_dir, file))
        if not file in committed_files:
            if not file in uncommited_files:
                untracked_files.append(file)
            else:
                if local_md5 != uncommited_files[file]:
                    modified_files.append(file)
        else:
            if local_md5 != committed_files[file]:
                if file in uncommited_files:
                    if local_md5 != uncommited_files[file]:
                        modified_files.append(file)
                else:
                    modified_files.append(file)
    modified_files.sort()
    untracked_files.sort()

    deleted_files = []
    for file in committed_files.keys():
        if not file in local_file_paths:
            if not file in uncommited_files or uncommited_files[file]:
                deleted_files.append(file)
    
    for file in uncommited_files.keys():
        if uncommited_files[file] and file not in local_file_paths:
            deleted_files.append(file)

    return committed_files, uncommited_files, modified_files, untracked_files, deleted_files
