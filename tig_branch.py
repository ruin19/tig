import re
from tig_common import *

def tig_branch(args):
    if len(args) == 1 :
        arg = args[0]
        if arg == "-v":
            show_branches()
        elif is_valid_path(arg):
            create_branch(arg)

def is_valid_path(path):
    pattern = r'^[a-zA-Z]+(/[a-zA-Z]+)*$'  # 匹配类似 "xx/yy/zz" 的路径格式

    if re.match(pattern, path):
        return True
    else:
        return False

def show_branches():
    heads_dir = tig_refs_heads_directory()
    current_branch_file = branch_file()
    for root, dirs, files in os.walk(heads_dir):
        for file in files:
            is_current_branch = False
            abs_path = os.path.join(root, file)
            if abs_path == current_branch_file:
                is_current_branch = True
            rel_path = os.path.relpath(abs_path, heads_dir)
            with open (abs_path, 'r') as file:
                md5 = file.read()
                commit_info = read_commit_or_tree_info(md5)
                if is_current_branch:
                    print("*", GREEN + rel_path + END, md5, commit_info["message"])
                else:
                    print(" ", rel_path, md5, commit_info["message"])

def create_branch(path):
    abs_path = os.path.join(tig_refs_heads_directory(), path)
    if not os.path.exists(abs_path):
        dir = os.path.dirname(abs_path)
        os.makedirs(dir, exist_ok=True)
        md5 = head_commit_md5()
        with open(abs_path, 'w') as file:
            file.write(md5)
