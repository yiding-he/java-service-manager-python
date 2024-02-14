import sys
from enum import Enum

from commands.helper import find_jar_file, find_lib_folder
from domain.config import Config


class JavaServiceType(Enum):
    FAT_JAR = "fat-jar"
    LIB_FOLDER = "lib-folder"


class JavaService:
    def __init__(self, data: dict):
        self.jar_path = None
        self.lib_folder = None
        self.data = data

    def get_type(self) -> JavaServiceType | None:
        self.jar_path = find_jar_file(self.data["root"])
        if self.jar_path is not None:
            return JavaServiceType.FAT_JAR

        self.lib_folder = find_lib_folder(self.data["root"])
        if self.lib_folder is not None:
            return JavaServiceType.LIB_FOLDER

        return None

    def get_name(self):
        return self.data["name"]


def get_service() -> JavaService | None:
    if len(sys.argv) < 3:
        print("Usage: jsm <command> <service> [options]")
        return None

    index_or_name = sys.argv[2]
    services = Config.CONFIG["jsm"]["services"]

    if index_or_name.isdigit():
        if not 0 <= int(index_or_name) < len(services):
            print("序号超出范围，请使用 jsm list 查看可用服务列表")
            return None
        return JavaService(services[int(index_or_name)])
