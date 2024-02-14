import glob
import logging
import os
import platform
import subprocess
import time

import psutil


def find_jar_file(path) -> str | None:
    # 使用glob.glob()函数查找path目录下的所有.jar文件
    jar_files = glob.glob(os.path.join(path, "*.jar"))

    # 如果找到了.jar文件，则返回第一个
    if jar_files:
        return jar_files[0].replace("\\", "/")
    else:
        return None  # 如果没有找到任何.jar文件，返回None


def find_lib_folder(path) -> str | None:
    # 使用glob.glob()函数查找path目录下的所有lib文件夹
    lib_folders = glob.glob(os.path.join(path, "lib/"))

    # 如果找到了lib文件夹，则返回第一个
    if lib_folders:
        return lib_folders[0].replace("\\", "/")
    else:
        return None  # 如果没有找到任何lib文件夹，返回None


def start_service_process(command: list[str], keywords: list[str]):
    """
    启动后台进程
    :param command: 启动命令，当中的 None 元素会自动忽略
    :param keywords: 启动过程中检查进程是否存在的搜索关键字
    """
    cleaned_command = [item for item in command if item is not None]
    print("--------------------")
    print(' '.join(cleaned_command))
    print("--------------------")

    process = None
    isWindows = platform.system() == 'Windows'
    if isWindows:
        process = subprocess.Popen(
            cleaned_command, universal_newlines=False,
            creationflags=subprocess.DETACHED_PROCESS
        )
    else:
        cleaned_command = ["bash", "-c", "nohup " + ' '.join(cleaned_command) + ">/dev/null &"]
        process = subprocess.Popen(
            cleaned_command, universal_newlines=False
        )

    print(f"进程启动中，进程ID为 {process.pid} ...")
    time.sleep(3)  # 如果是 JVM 参数问题导致无法启动，那么 3 秒内进程应该会结束

    # 如果 3 秒后进程还在，说明 JVM 启动成功，但有可能之后因为框架初始化失败而退出。
    # 所以这里执行完后应该持续观察服务日志，确认日志当中包含服务完全启动的信息。
    search_result = search_service_process(keywords)
    if len(search_result) > 0:
        print("进程启动成功")
    elif not isWindows:
        print(f"进程启动失败")


def search_service_process(keywords: list[str]) -> list[dict]:
    """
    根据关键字查询进程
    :param keywords: 关键字列表，通过任何一个查到了就表示满足条件
    """
    
    # 获取所有运行中的进程
    processes = psutil.process_iter(['pid', 'name', 'cmdline'])

    # 搜索包含关键字的进程
    matching_processes = []
    for process in processes:
        try:
            # cmdline可能为None，需要处理异常
            if process.info['cmdline'] and any(k in ' '.join(process.info['cmdline']) for k in keywords):
                matching_processes.append({
                    'pid': process.info['pid'],
                    'name': process.info['name'],
                    'cmdline': ' '.join(process.info['cmdline'])
                })
        except (psutil.NoSuchProcess, KeyError):
            pass

    return matching_processes


def kill_service_process(pid: int, timeout_sec: int = 10):
    """
    杀死指定进程
    :param pid: 进程ID
    :param timeout_sec: 等待超时时间，如果进程在超时时间内没有结束，则强制杀死进程
    """
    # 尝试获取指定PID的进程对象
    process = psutil.Process(pid)

    # 首先尝试优雅地结束进程（发送SIGTERM信号）
    logging.info(f"尝试结束进程 {pid} ...")
    process.terminate()

    # 等待进程结束（可以设定一个合理的超时时间，这里为5秒）
    try:
        process.wait(timeout=timeout_sec)
    except psutil.TimeoutExpired:
        # 如果在超时时间内进程未结束，则强制结束该进程（发送SIGKILL信号）
        process.kill()

    # 这里确认进程是否已经结束
    if not process.is_running():
        logging.info(f"进程 {pid} 已经结束")
    else:
        logging.error(f"进程 {pid} 未能结束")
