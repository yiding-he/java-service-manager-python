import sys
import os
import socket
from enum import Enum

from commands.helper import find_jar_file, find_lib_folder
from domain.config import Config


class JavaServiceType(Enum):
    FAT_JAR = "fat-jar"
    LIB_DIR = "lib-dir"


class JavaService:
    def __init__(self, data: dict):
        self.jar_path = None
        self.lib_folder = None
        self.data = data
        self.type = None

        self.__init_type__()

    def __init_type__(self):
        if self.type is None:
            self.jar_path = find_jar_file(self.data["root"])
            if self.jar_path is not None:
                self.type = JavaServiceType.FAT_JAR

            self.lib_folder = find_lib_folder(self.data["root"])
            if self.lib_folder is not None:
                self.type = JavaServiceType.LIB_DIR

    def get_type(self) -> JavaServiceType | None:
        return self.type

    def get_search_keywords(self) -> list[str]:
        # 通过 config 目录查找可以避免混淆 service 和 service-1
        return [
            os.path.join(self.get_root(), "config")
        ]

    def get_name(self):
        """
        查询服务名称。如果指定了 name，则使用它，
        否则使用根目录作为服务名称
        """
        if "name" in self.data:
            return self.data["name"]
        else:
            return self.data["root"]

    def get_executable(self):
        """
        查询 java命令路径。如果指定了 executable，则使用它，
        否则检查是否指定了 java_home 并用来拼接 java 命令，
        如果没有则尝试直接使用 "java" 命令
        """
        executable_path = "java"
        if "executable" in self.data:
            executable_path = self.data["executable"]
        if "java_home" in self.data:
            executable_path = f"{self.data['java_home']}/bin/java"

        return (executable_path
                .replace("/", os.sep)
                .replace("\\", os.sep))

    def get_jvm_args(self) -> list[str] | None:
        if "jvm_args" in self.data:
            return str(self.data["jvm_args"]).split(" ")
        else:
            return None

    def get_app_args(self) -> list[str] | None:
        if "app_args" in self.data:
            return str(self.data["app_args"]).split(" ")
        else:
            return None

    def get_root(self) -> str | None:
        if "root" in self.data:
            return self.data["root"]
        else:
            return None
        
    def get_config_dir(self) -> str:
        if "config_dir" in self.data:
            return str(self.data["config_dir"]).replace("${root}", self.get_root())
        else:
            return os.path.join(self.get_root(), "config")

    def get_log_dir(self) -> str:
        if "log_dir" in self.data:
            hostname = socket.gethostname()
            log_dir = str(self.data["log_dir"]).replace("${root}", self.get_root())
            log_dir = os.path.join(log_dir, hostname)
        else:
            log_dir = os.path.join(self.get_root(), "logs", hostname)
        return log_dir
        
    def get_log_file_name(self) -> str:
        hostname = socket.gethostname()
        return "server-" + hostname

    def get_log_file(self) -> str | None:
        return os.path.join(self.get_log_dir(), self.get_log_file_name() + ".log")

    def get_terminate_timeout(self) -> int | None:
        if "terminate_timeout" in self.data:
            return int(self.data["terminate_timeout"])
        else:
            return None


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
