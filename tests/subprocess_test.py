import subprocess
import time


def run_process_sync():
    with subprocess.Popen(jar_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) as process:
        for line in process.stdout:
            print(line, end='')
        process.wait()
        if process.returncode == 0:
            print("Java程序成功执行")
        else:
            print(f"Java程序执行失败，退出码为 {process.returncode}")


def run_process_async(command: list[str]):
    process = subprocess.Popen(
        command, universal_newlines=False,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        creationflags=subprocess.DETACHED_PROCESS
    )
    print(f"进程启动中，进程ID为 {process.pid} ...")
    time.sleep(3)

    poll = process.poll()
    if poll is None:
        print("进程启动成功")
    else:
        print(f"进程启动失败，退出码为 {poll}")


if __name__ == '__main__':
    # Java命令行参数列表
    jar_command = ['java', '-jar',
                   '../java-projects/fat-jar/java-sample-project-1.0-SNAPSHOT.jar',
                   '--spring.profiles.active=dev'
                   ]

    run_process_async(jar_command)
    print("run_process_async() finished.")
