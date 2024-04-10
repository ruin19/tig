import os

def tig_init():
    create_tig_directory()

def create_tig_directory():
    current_dir = os.getcwd()
    tig_dir = os.path.join(current_dir, '.tig')

    if os.path.exists(tig_dir):
        print(tig_dir + "仓库已存在，无需初始化")
        return
    else:
        os.mkdir(tig_dir)

    objects_dir = os.path.join(tig_dir, 'objects')
    os.mkdir(objects_dir)

    refs_dir = os.path.join(tig_dir, 'refs')
    os.mkdir(refs_dir)

    refs_heads_dir = os.path.join(refs_dir, 'heads')
    os.mkdir(refs_heads_dir)

