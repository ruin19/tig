import copy
from tig_common import *
from tig_tree import *

class Committer:
    path_node_dict = {}
    tree = None

    def __init__(self) -> None:
        pass

    def commit(self):
        data = read_uncommited_files()
        if not bool(data):
            return

        self.tree = Tree()
        self.tree.load_commit_tree()

        keys = list(data.keys())
        sorted_keys = sorted(keys, reverse=True)

        for path in sorted_keys:
            self.process(path, data[path])
        
        for node in self.path_node_dict.values():
            node.save_to_file()
        
        self.save_commit_info_to_file()

        # 清空未提交文件的记录
        save_uncommited_files({})


    def process(self, file_path, md5):
        """
        处理一个uncommited文件, 更新树节点
        """
        self.update_node(file_path, md5, NodeType.BLOB, None)

    
    def update_node(self, path, md5, node_type, child):
        """
        递归地创建或更新树节点, 如果是blob类型, child可以是空. 如果是tree类型, md5可以是空, 自己负责计算
        """
        name = path.rsplit("/", 1)[-1]
        parent_dir = os.path.dirname(path) 
        # print("update_node parent_dir: " + parent_dir + " name: " + name)
        if node_type == NodeType.BLOB:
            node = TreeNode(name, md5, node_type)
            self.path_node_dict[path] = node
        else:
            node = self.path_node_dict.get(path)
            if node:
                node.add_child(child)
                node.update_md5()
            else:
                old_node = self.tree.node_of_path(path)
                node = None
                if old_node:
                    node = copy.copy(old_node)
                else:
                    node = TreeNode(name, "", NodeType.TREE)
                self.path_node_dict[path] = node
                node.add_child(child)
                node.update_md5()

        if path:
            self.update_node(parent_dir, "", NodeType.TREE, node)

    def save_commit_info_to_file(self):
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
        # 上一次commit的md5
        parent_commit_md5 = head_commit_md5()
        if parent_commit_md5:
            data["parent"] = [{"md5": parent_commit_md5}]
        save_commit_info(data)



        

def tig_commit():
    committer = Committer()
    committer.commit()
