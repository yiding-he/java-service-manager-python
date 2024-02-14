import logging
import logging.config
import os
from pathlib import Path

import yaml


class Config:
    CONFIG = None
    CONFIG_FILE_NAME = ".jsm.yaml"
    CONFIG_FILE_PATH = None

    @staticmethod
    def find_jsm_yaml_file():
        candidate = os.path.join(os.path.expanduser("~"), ".jsm.yaml")
        if os.path.isfile(candidate):
            return candidate

        candidate = os.path.join(os.getcwd(), ".jsm.yaml")
        if os.path.isfile(candidate):
            return candidate
        else:
            Path(candidate).touch(exist_ok=True)
        return candidate

    @classmethod
    def load_config(cls):
        if cls.CONFIG is None:
            cls.CONFIG_FILE_PATH = Config.find_jsm_yaml_file()
            logging.debug("加载配置文件 %s", cls.CONFIG_FILE_PATH)
            with open(cls.CONFIG_FILE_PATH, "r") as f:
                cls.CONFIG = yaml.safe_load(f)
            if cls.CONFIG is None:
                cls.CONFIG = {"jsm": {"services": []}}
            if cls.CONFIG["jsm"] is None:
                cls.CONFIG["jsm"] = {"services": []}

    @classmethod
    def save_config(cls):
        if cls.CONFIG is None:
            logging.error("未加载配置文件")
            return
        if cls.CONFIG_FILE_PATH is None:
            logging.error("未找到配置文件 .jsm.yaml")
            return
        with open(cls.CONFIG_FILE_PATH, "w") as f:
            f.write(yaml.dump(cls.CONFIG, default_flow_style=False, indent=2))

    @classmethod
    def init_logging(cls):
        log_config = {
            'version': 1,  # 配置文件版本号
            'disable_existing_loggers': False,  # 是否禁用已存在的日志器，默认False
            'formatters': {  # 格式化器，这里没有定义则使用默认格式
                'standard': {  # 自定义名称的格式化器，这里未使用
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                },
            },
            'handlers': {  # 处理器配置
                'console': {  # 输出到控制台的处理器
                    'class': 'logging.StreamHandler',  # 使用StreamHandler类处理日志
                    'level': 'INFO',  # 设置处理器的日志级别
                    'formatter': 'standard',  # 如果有自定义格式，可指定此字段
                    'stream': 'ext://sys.stdout',  # 指定输出流为标准输出
                },
            },
            'root': {  # 根logger配置
                'level': 'INFO',  # 设置根logger的日志级别
                'handlers': ['console'],  # 指定要使用的处理器列表
            },
        }
        logging.config.dictConfig(log_config)
