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
    objects_dir = tig_objects_directory()
    file_path = os.path.join(objects_dir, file_md5)
    if os.path.exists(file_path):
        print_zip_file(file_path)
    else:
        print("md5: " + file_md5 + " not exist")


def print_zip_file(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        extracted_file = zipf.namelist()[0]
        with zipf.open(extracted_file, 'r') as file:
            content = file.read().decode('utf-8')
            print(content)