from domain.service import JavaServiceType, JavaService, get_service


def start_lib_folder(service: JavaService):
    pass


def start_fat_jar(service: JavaService):
    pass


def start_command():
    service = get_service()
    if service is None:
        return

    service_type = service.get_type()
    if service_type == JavaServiceType.FAT_JAR:
        start_fat_jar(service)
    elif service_type == JavaServiceType.LIB_FOLDER:
        start_lib_folder(service)
    else:
        print(f"无法确定服务 {service.get_name()} 的启动方式")
