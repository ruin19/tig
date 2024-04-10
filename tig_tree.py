import hashlib
from enum import Enum
from tig_common import *

class NodeType(Enum):
    TREE = 1
    BLOB = 2

class TreeNode:
    name = None
    md5 = None
    node_type = NodeType.TREE
    children = []

    def __init__(self, name, md5, node_type):
        self.name = name 
        self.md5 = md5
        self.node_type = node_type
        self.children = []
        print("create Node name: " + name)

    def add_child(self, child):
        for my_child in self.children:
            if my_child.name == child.name:
                self.children.remove(my_child)
                break
        self.children.append(child)

    def merge_from_node_if_not_exist(self, node):
        """
        其他节点合并给自己, 如果存在同样的children, 以自己为准
        """
        if not node:
            return

        for other_child in node.children:
            found = False
            for my_child in self.children:
                if my_child.name == other_child.name:
                    found = True
                    break
            if not found:
                self.children.append(other_child)

    def description(self):
        nodes = []
        for child in self.children:
            node = {}
            node["name"] = child.name
            node["md5"] = child.md5
            if child.node_type == NodeType.TREE:
                node["type"] = "tree"
            else:
                node["type"] = "blob"
            nodes.append(node)
        return {"nodes": nodes}

    def update_md5(self):
        desc = self.description()
        # print(desc)
        str = json.dumps(desc, sort_keys=True)
        self.md5 = hashlib.md5(str.encode()).hexdigest()
    
    def save_to_file(self):
        if self.node_type == NodeType.TREE:
            save_commit_or_tree_info(self.description())

class Tree:
    rootNode = None

    def __init__(self) -> None:
        pass

    def load_commit_tree(self):
        """
        加载当前commit对应的树结构
        """
        commit_info = read_commit_info()
        if not commit_info:
            return
        
        # print(commit_info)
        root_md5 = commit_info["md5"]
        if not root_md5:
            return
        
        self.rootNode = self.load_tree_from_md5("", root_md5)


    def load_tree_from_md5(self, name, md5):
        """
        从objects加载指定md5对应的树, 因为树的名字存储在上级目录，因此需要外部传入
        """
        node = TreeNode(name, md5, NodeType.TREE)
        tree_info = read_commit_or_tree_info(md5)
        for child in tree_info["nodes"]:
            if child["type"] == "tree":
                child_node = self.load_tree_from_md5(child["name"], child["md5"])
                node.add_child(child_node)
            else:
                child_node = TreeNode(child["name"], child["md5"], NodeType.BLOB)
                node.add_child(child_node)
        return node

    def node_of_path(self, path):
        """
        给定目录，返回对应的树节点
        """

        if not self.rootNode:
            return None

        if not path:
            return self.rootNode

        path_parts = path.split("/")
        return self.node_of_path_parts(path_parts, self.rootNode)

    def node_of_path_parts(self, path_parts, node):
        """
        给定数组表示的分段路径，返回对应的树节点
        """
        if not path_parts:
            return node

        part = path_parts[0]
        for child in node.children:
            if child.name == part:
                return self.node_of_path_parts(path_parts[1:], child)

        return None