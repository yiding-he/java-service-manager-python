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

    try:
        with subprocess.Popen(
            ["tail", "-fn100", service.get_log_file()], 
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True
        ) as process:
            for line in process.stdout:
                print(line, end='')
            process.wait()
    except KeyboardInterrupt:
        sys.exit(0)

