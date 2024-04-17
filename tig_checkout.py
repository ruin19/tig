from tig_common import *

def tig_checkout(args):
    arg = args[0]
    branches = branch_names()
    if arg in branches:
        content = os.path.join("refs/heads", arg)
        head_pointer = head_pointer_file()
        with open(head_pointer, 'w') as file:
            file.write(content)
        print("Switch to branch " + arg)