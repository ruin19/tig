import subprocess
from tig_common import *

def tig_log():
    commit_info = read_commit_info()
    content = ""
    while(commit_info):
        content += content_from_commit_info(commit_info)
        parents = commit_info.get("parent")
        if not parents:
            break
        # TODO: 暂时只取第一个
        last_commit_md5 = parents[0]["md5"]
        commit_info = read_commit_or_tree_info(last_commit_md5)
    
    print(content)
    less_process = subprocess.Popen(['less'], stdin=subprocess.PIPE)
    less_process.communicate(input=content.encode())

def content_from_commit_info(commit_info):
    content = ""
    content += "\ncommit " + commit_info["md5"]
    content += "\nDate:\t" + commit_info["time"]
    content += "\n\t" + commit_info["message"]
    content += "\n"
    return content