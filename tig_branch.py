import re
from tig_common import *

def tig_branch(args):
    if len(args) == 1 :
        path = args[0]
        if is_valid_path(path):
            abs_path = os.path.join(tig_refs_heads_directory(), path)
            if not os.path.exists(abs_path):
                dir = os.path.dirname(abs_path)
                os.makedirs(dir, exist_ok=True)
                md5 = head_commit_md5()
                with open(abs_path, 'w') as file:
                    file.write(md5)
            

def is_valid_path(path):
    pattern = r'^[a-zA-Z]+(/[a-zA-Z]+)*$'  # 匹配类似 "xx/yy/zz" 的路径格式

    if re.match(pattern, path):
        return True
    else:
        return False