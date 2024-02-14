import glob
import os


def find_jar_file(path) -> str | None:
    # 使用glob.glob()函数查找path目录下的所有.jar文件
    jar_files = glob.glob(os.path.join(path, "*.jar"))

    # 如果找到了.jar文件，则返回第一个
    if jar_files:
        return jar_files[0]
    else:
        return None  # 如果没有找到任何.jar文件，返回None


def find_lib_folder(path) -> str | None:
    # 使用glob.glob()函数查找path目录下的所有lib文件夹
    lib_folders = glob.glob(os.path.join(path, "lib/"))

    # 如果找到了lib文件夹，则返回第一个
    if lib_folders:
        return lib_folders[0]
    else:
        return None  # 如果没有找到任何lib文件夹，返回None
