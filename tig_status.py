import os
from tig_common import *
from tig_tree import *

def tig_status():
    tree = Tree()
    tree.load_commit_tree()
    # 已提交的 文件 - md5 映射
    commit_file_paths = tree.file_paths()
    # if commit_file_paths:
    #     print("committed files:")
    #     for file, md5 in commit_file_paths.items():
    #         print("\t" + file + "\t" + md5)

    # 暂存区的 文件 - md5 映射
    uncommited_files = read_uncommited_files()

    # 本地文件数组
    local_file_paths = set(local_files())

    # 打印暂存区文件
    if uncommited_files:
        print("Changes to be committed:")
        for file in uncommited_files.keys():
            if file in commit_file_paths:
                print(GREEN + "\tmodified\t" + file + END)
            else:
                print(GREEN + "\tnew file\t" + file + END)

    untracked_files = []
    modified_files = []
    for file in local_file_paths:
        local_md5 = file_md5(file)
        if not file in commit_file_paths:
            if not file in uncommited_files:
                untracked_files.append(file)
            else:
                if local_md5 != uncommited_files[file]:
                    modified_files.append(file)
        else:
            if local_md5 != commit_file_paths[file]:
                if file in uncommited_files:
                    if local_md5 != uncommited_files[file]:
                        modified_files.append(file)
                else:
                    modified_files.append(file)

    # 打印修改后未提交暂存区的文件
    if modified_files:
        print("Changes not staged for commit:")
        for file in modified_files:
            print(RED + "\t" + file + END)

    # 打印新增的未提交暂存区的文件
    if untracked_files:
        print("Untracked files:")
        for file in untracked_files:
            print(RED + "\t" + file + END)