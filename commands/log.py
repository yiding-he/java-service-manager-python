import platform
import logging
import subprocess
import signal
import sys

from domain.service import get_service


def log_command():
    isWindows = platform.system() == 'Windows'
    if isWindows:
        logging.error("Windows 尚不支持")
        return

    service = get_service()
    if service is None:
        logging.error("未指定要操作的服务")
        return

    with subprocess.Popen(
        ["tail", "-fn100", service.get_log_file()], 
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
    ) as process:
        try:
            for line in process.stdout:
                print(line, end='')
        except KeyboardInterrupt:
            logging.info("结束查看日志")
            sys.exit(0)

        process.wait()
