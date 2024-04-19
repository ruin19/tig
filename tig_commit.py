import copy
from datetime import datetime
from tig_common import *
from tig_tree import *


class Committer:
    path_node_dict = {}
    tree = None

    def __init__(self) -> None:
        pass

    def commit(self, message):
        data = read_uncommited_files()
        if not bool(data):
            return

        self.tree = Tree()
        self.tree.load_commit_tree()

        keys = list(data.keys())
        sorted_keys = sorted(keys, reverse=True)

        for path in sorted_keys:
            self.process_file(path, data[path])

        for node in self.path_node_dict.values():
            node.save_to_file()
        
        self.save_commit_info_to_file(message)

        # 清空未提交文件的记录
        save_uncommited_files({})


    def process_file(self, file_path, md5):
        """
        处理一个uncommited文件, 更新树节点
        """
        self.update_node(file_path, md5, NodeType.BLOB, None, None)

    def update_node(self, path, md5, node_type, child, delete_name):
        """
        从叶子节点向父节点递归地创建/更新树节点
        如果是blob类型, child是空. md5非空表示新增或修改的文件节点, 为空则是删除的文件
        如果是tree类型, md5是空, 自己负责计算. child非空表示新增的子节点, child为空且delete_name存在则表示删除一个子节点
        """
        name = path.rsplit("/", 1)[-1]
        parent_dir = os.path.dirname(path) 
        # print("update_node parent_dir: " + parent_dir + " name: " + name + " node_type: ", node_type)
        node = None
        if node_type == NodeType.BLOB:
            if md5:
                node = TreeNode(name, md5, NodeType.BLOB)
                self.path_node_dict[path] = node
                delete_name = None
            else:
                delete_name = name
        else:
            node = self.path_node_dict.get(path)
            if not node:
                old_node = self.tree.node_of_path(path)
                node = None
                if old_node:
                    node = copy.copy(old_node)
                else:
                    node = TreeNode(name, "", NodeType.TREE)
                self.path_node_dict[path] = node
            if child:
                node.add_child(child)
            elif delete_name:
                node.remove_child_by_name(delete_name)
            node.update_md5()

        if path:
            self.update_node(parent_dir, "", NodeType.TREE, node, delete_name)

    def save_commit_info_to_file(self, message):
        """
        更新objects/[commit文件]
        """
        # 树根节点
        root_node = None
        for node in self.path_node_dict.values():
            if not node.name:
                root_node = node
                break
        
        if not root_node:
            return
        
        data = {"md5": root_node.md5} 
        # print(message)
        data["message"] = message

        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        data["time"] = formatted_datetime
        # 上一次commit的md5
        parent_commit_md5 = head_commit_md5()
        if parent_commit_md5:
            data["parent"] = [{"md5": parent_commit_md5}]
        save_commit_info(data)
        

def tig_commit(option, message):
    if option == '-m':
        committer = Committer()
        committer.commit(message)
    else:
        print("Invalid option. Please use '-m'")
