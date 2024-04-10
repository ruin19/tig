import os
import json
import hashlib

def tig_directory():
    """
    返回.tig路径
    会在当前目录一直往上一直找到为止，否则返回空
    """
    current_dir = os.getcwd()

    while True:
        tig_dir = os.path.join(current_dir, '.tig')
        if os.path.exists(tig_dir):
            return tig_dir

        # 到达根目录，停止查找
        if current_dir == os.path.dirname(current_dir):
            break

        current_dir = os.path.dirname(current_dir)

    return None


def project_directory():
    """
    返回含有.tig的仓库路径
    """
    tig_dir = tig_directory()
    if not tig_dir:
        return None
    return os.path.dirname(tig_dir)

def tig_objects_directory():
    """
    返回.tig/objects的路径
    """
    tig_dir = tig_directory()
    if not tig_dir:
        return None
    
    objects_dir = os.path.join(tig_dir, 'objects')
    if os.path.exists(objects_dir):
        return objects_dir
    else:
        return None

def tig_refs_directory():
    """
    返回.git/refs的路径
    """
    tig_dir = tig_directory()
    if not tig_dir:
        return None
    
    refs_dir = os.path.join(tig_dir, 'refs')
    if os.path.exists(refs_dir):
        return refs_dir 
    else:
        return None

def tig_refs_heads_directory():
    """
    返回.git/refs/heads的路径
    """
    refs_dir = tig_refs_directory()
    if not refs_dir:
        return None

    heads_dir = os.path.join(refs_dir, 'heads')
    if os.path.exists(heads_dir):
        return heads_dir
    else:
        return None

def main_file():
    """
    返回.git/refs/heads/main的文件路径
    """
    refs_heads_dir = tig_refs_directory()
    if not refs_heads_dir:
        return None
    
    main_file_path = os.path.join(refs_heads_dir, 'main')
    if not os.path.exists(main_file_path):
        with open (main_file_path, 'w') as file:
            pass
    return main_file_path

def index_file():
    """
    返回.git/index的文件路径
    """
    tig_dir = tig_directory()
    if not tig_dir:
        return None
    
    index_file_path = os.path.join(tig_dir, 'index')
    if not os.path.exists(index_file_path):
        with open(index_file_path, 'w') as file:
            pass
    return index_file_path

def read_uncommited_files():
    """
    读取.git/index文件内容
    index文件保存了已add未commit的文件信息, 类似: 
    {
      "aaa/3.txt": "ec2824fec1a1e325ca2d29d9313244db",
      "1.txt": "23cdc18507b52418db7740cbb5543e54",
      "2.txt": "d41d8cd98f00b204e9800998ecf8427e"
    }
    """
    index_file_path = index_file()
    try:
        with open(index_file_path, 'r') as file:
            data = json.load(file)
            return data
    except json.decoder.JSONDecodeError:
        return {}

def save_uncommited_files(data):
    """
    保存已add未commit的文件信息到.git/index文件
    """
    index_file_path = index_file()
    with open(index_file_path, 'w') as file:
        json.dump(data, file)

def head_commit_md5():
    """
    返回refs/headers/main指针指向的commit的md5
    """

    # 暂未考虑分支，直接从main中读
    main_file_path = main_file()
    if not main_file_path:
        return None
    with open (main_file_path, 'r') as file:
        content = file.read()
        if not content:
            return None
        # content = content.decode('utf-8')
        return content

def read_commit_or_tree_info(md5):
    """
    读取commit文件或tree文件的内容

    commit文件内容类似:
    {
      "md5": "1645257b2614938d30d3bd3f3eaee5950108769c",
      "parent": [
        {
          "md5": "fc0dd6844a568679bd41a33495ecaf8c93edbec7"
        },
        {
          "md5": "e368d877b053d907fa8dc8e81b9dd5cd"
        }
      ]
    }

    tree文件内容类似:
    {
        "nodes": [
            {
                "name": "aaa",
                "md5": "1645257b2614938d30d3bd3f3eaee5950108769c",
                "type": "tree"
            },
            {
                "name": "1.txt",
                "md5": "81c545efebe5f57d4cab2ba9ec294c4b0cadf672",
                "type": "blob"
            }
        ]
    }
    """
    file_path = os.path.join(tig_objects_directory(), md5)
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except json.decoder.JSONDecodeError:
        return {}    

def save_commit_or_tree_info(data):
    """
    保存commit信息或tree信息到文件
    """
    str = json.dumps(data, sort_keys=True)
    md5_hash = hashlib.md5(str.encode()).hexdigest()
    file_path = os.path.join(tig_objects_directory(), md5_hash)
    with open (file_path, 'w') as file:
        file.write(str)
        print("saving file: " + file_path + " content: " + str)

    return md5_hash

def read_commit_info():
    """
    读取commit文件的内容
    """
    commit_md5 = head_commit_md5()
    if not commit_md5:
        return None

    return read_commit_or_tree_info(commit_md5)

def save_commit_info(data):
    """
    保存commit信息到commit文件
    """
    md5_hash = save_commit_or_tree_info(data)

    # 更新refs/headers/main指针的哈希值
    with open (main_file(), 'w') as file:
        file.write(md5_hash)
