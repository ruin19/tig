import os
import zipfile

from tig_common import *

def tig_catfile(option, file_md5):
    if option == '-p':
        print_file_content(file_md5)
    elif option == '-t':
        # 打印文件类型
        pass
    else:
        print("Invalid option. Please use '-p' or '-t'.")

def print_file_content(file_md5):
    print(md5_file_content(file_md5))

def md5_file_content(file_md5):
    """
    返回.tig/objects目录下指定md5文件的内容
    """
    objects_dir = tig_objects_directory()
    file_path = os.path.join(objects_dir, file_md5)
    if os.path.exists(file_path):
        return zip_file_content(file_path)
    else:
        return None

def zip_file_content(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        extracted_file = zipf.namelist()[0]
        with zipf.open(extracted_file, 'r') as file:
            content = file.read().decode('utf-8')
            return content