
import logging
from commands.helper import search_service_process
from domain.service import get_service


def status_command():
    service = get_service()
    if service is None:
        logging.error("未指定要操作的服务")
        return
    
    search_result = search_service_process(service.get_search_keywords())
    if len(search_result) > 0:
        logging.info(f"服务 {service.get_name()} 已经在运行中，PID 为 {search_result[0]['pid']}")
    else:
        logging.info(f"服务 {service.get_name()} 没有运行。")
