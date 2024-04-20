import difflib
from tig_status import *
from tig_catfile import *

def tig_diff(args):
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
    diff(paths)

def diff(paths):
    """
    打印指定目录或文件的diff,若不指定,则是仓库下所有的diff
    """
    commited_files, uncommited_files, modified_files, untracked_files, deleted_files = fetch_status()
    diff_files = modified_files 
    if paths:
        # 有路径限制的情况
        diff_files = [path for path in diff_files if any(path.startswith(prefix) for prefix in paths)]
    project_dir = project_directory()
    for file in diff_files:
        md5 = ""
        if file in uncommited_files:
            md5 = uncommited_files[file]
        else:
            md5 = commited_files[file]
        f1_content = md5_file_content(md5)

        file_abs = os.path.join(project_dir, file)
        with open(file_abs, "r", encoding='utf-8') as f2:
            lines1 = f1_content.splitlines()
            lines2 = f2.read().splitlines()
        
        diff = difflib.unified_diff(lines1, lines2, fromfile="a/"+file, tofile="b/"+file)
        for line in diff:
            if line.startswith('-'):
                print(RED + line + END)
            elif line.startswith('+'):
                print(GREEN + line + END)
            else:
                print(line)
        print("\n")