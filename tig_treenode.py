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

    def add_child(self, child):
        for my_child in self.children:
            if my_child.name == child.name:
                self.children.remove(my_child)
                break
        self.children.append(child)

    def remove_child_by_name(self, name):
        for my_child in self.children:
            if my_child.name == name:
                self.children.remove(my_child)
                break

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