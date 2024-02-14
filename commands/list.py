import textwrap

from domain.config import Config


def list_command():
    services = Config.CONFIG["jsm"]["services"]
    index_len = 1 if len(services) < 9 else 2 if len(services) < 99 else 3
    name_len = max(len(service["name"]) for service in services)
    if services:
        print(f"找到 {len(services)} 个服务: ")
        for i in range(len(services)):
            service = services[i]
            print(("  [{:" + str(index_len) + "d}] {:" + str(name_len) + "} ({})")
                  .format(i, service["name"], service["root"]))
        print(textwrap.dedent("""
            请使用服务序号或者服务名来操作服务。
            例如: jsm start service1
            如果服务名存在重复，则只能通过序号来指定。
            例如: jsm start 0"""))
    else:
        print("没有找到任何服务，请使用 jsm add 添加服务所在的文件夹路径")
