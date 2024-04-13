import difflib
from tig_status import *
from tig_catfile import *

def tig_diff():
    commited_files, uncommited_files, modified_files, untracked_files = fetch_status()
    project_dir = project_directory()
    for file in modified_files:
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