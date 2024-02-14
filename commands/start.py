import logging

from commands.helper import start_service_process, search_service_process
from domain.service import JavaServiceType, JavaService, get_service


def start_lib_dir(service: JavaService):
    logging.info(f"启动服务 {service.get_name()}...")
    logging.info(f"服务类型为 {service.get_type()}")
    logging.info(f"打包路径为 {service.jar_path}")
    logging.info(f"日志输出路径为 {service.get_log_file()}")

    java_executable = service.get_executable()
    logging.info(f"java 执行路径为 {java_executable}")
    pass


def start_fat_jar(service: JavaService):
    logging.info(f"启动服务 {service.get_name()}...")
    logging.info(f"服务类型为 {service.get_type()}")
    logging.info(f"打包路径为 {service.jar_path}")
    logging.info(f"日志输出路径为 {service.get_log_file()}")

    java_executable = service.get_executable()
    logging.info(f"java 执行路径为 {java_executable}")

    service_name_arg = "-Dservice.name=" + service.get_name()
    log_dir_arg = ("-Dlog.root=" + service.get_log_dir()) if service.get_log_dir() is not None else None
    log_file_arg = "-Dlog.file=" + service.get_log_file_name()
    config_dir_arg = "--spring.config.additional-location=" + service.get_config_dir() + "/"
    
    command = ([java_executable, service_name_arg, log_dir_arg, log_file_arg] + service.get_jvm_args() +
               ["-jar", service.jar_path] + service.get_app_args() + [config_dir_arg])

    search_keywords = service.get_search_keywords()
    search_result = search_service_process(search_keywords)
    if len(search_result) > 0:
        logging.error(f"服务 {service.get_name()} 已经在运行中，PID 为 {search_result[0]['pid']}")
        return
    start_service_process(command, search_keywords)


def start_command():
    service = get_service()
    if service is None:
        logging.error("未指定要操作的服务")
        return

    service_type = service.get_type()
    if service_type == JavaServiceType.FAT_JAR:
        start_fat_jar(service)
    elif service_type == JavaServiceType.LIB_DIR:
        start_lib_dir(service)
    else:
        print(f"无法确定服务 {service.get_name()} 的启动方式")
