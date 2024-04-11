from tig_common import *
from tig_treenode import *

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

    def file_paths(self):
        paths = []
        if self.rootNode:
            self.file_paths_of_node(paths, self.rootNode, "")
        paths.sort()
        return paths


    def file_paths_of_node(self, paths, node, prefix):
        if prefix:
            prefix = prefix + "/" + node.name
        else:
            prefix = node.name

        if node.node_type == NodeType.BLOB:
            paths.append(prefix)
        else:
            for child in node.children:
                self.file_paths_of_node(paths, child, prefix)
