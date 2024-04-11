import os
from tig_common import *
from tig_tree import *

def tig_status():
    tree = Tree()
    tree.load_commit_tree()
    commit_file_paths = set(tree.file_paths())

    local_file_paths = set(local_files())

    uncommited_files = []
    uncommited_data = read_uncommited_files()
    if uncommited_data:
        uncommited_files = set(uncommited_data.keys())

    print("Changes to be committed:")
    print("\t", uncommited_files)

    untracked_files = []

    for file in local_file_paths:
        if not file in commit_file_paths:
            if not file in uncommited_files:
                untracked_files.append(file)

    print("Untracked files:")
    print("\t", untracked_files)