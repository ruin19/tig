from tig_common import *
from tig_status import *
from tig_catfile import *

# TODO 支持丢弃本地修改和删除操作
def tig_checkout(args):
    if len(args) == 1:
        arg = args[0]
        branches = branch_names()
        if arg in branches:
            checkout_branch(arg)
            return

    paths = []
    project_dir = project_directory()
    for arg in args:
        if arg == ".":
            # 只要有一个通配符，就丢弃所有指定路径，paths设置为空，表示无需任何匹配条件
            paths.clear()
            break
        if not os.path.exists(arg):
            continue
        
        abs_path = os.path.join(os.getcwd(), arg)
        rel_path = os.path.relpath(abs_path, project_dir)
        paths.append(rel_path)
    checkout_path(paths)

def checkout_branch(branch):
    """
    切换分支
    """
    content = os.path.join("refs/heads", branch)
    head_pointer = head_pointer_file()
    with open(head_pointer, 'w') as file:
        file.write(content)
    print("Switch to branch " + branch)
    

def checkout_path(paths):
    """
    丢弃指定文件,或指定目录下的文件
    """
    commited_files, uncommited_files, modified_files, untracked_files, deleted_files = fetch_status()
    restore_files = modified_files + deleted_files
    if paths:
        # 有路径限制的情况
        restore_files = [path for path in restore_files if any(path.startswith(prefix) for prefix in paths)]

    project_dir = project_directory()
    for file in restore_files:
        md5 = ""
        if file in uncommited_files:
            md5 = uncommited_files[file]
        else:
            md5 = commited_files[file]
        f1_content = md5_file_content(md5)

        file_abs = os.path.join(project_dir, file)
        with open(file_abs, "w", encoding='utf-8') as f2:
            f2.write(f1_content)
    print("Updated", len(restore_files), "paths from the index")