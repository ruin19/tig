from tig_common import *

def tig_log():
    commit_info = read_commit_info()
    while(commit_info):
        print_commit_info(commit_info)
        parents = commit_info.get("parent")
        if not parents:
            return
        # TODO: 暂时只取第一个
        last_commit_md5 = parents[0]["md5"]
        commit_info = read_commit_or_tree_info(last_commit_md5)

def print_commit_info(commit_info):
    print("commit ", commit_info["md5"])
    print("Date:\t", commit_info["time"])
    print("\t", commit_info["message"])
    print("\n")