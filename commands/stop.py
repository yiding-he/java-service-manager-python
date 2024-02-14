from commands.helper import search_service_process, kill_service_process
from domain.service import get_service
import logging


def stop_command():
    service = get_service()
    if service is None:
        logging.error("未指定要操作的服务")
        return

    process = search_service_process(service.get_search_keyword())
    if len(process) == 0:
        logging.error(f"服务 {service.get_name()} 不在运行中")
        return

    kill_service_process(process[0]['pid'])
