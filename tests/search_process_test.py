from commands.helper import search_service_process

if __name__ == '__main__':
    process = search_service_process(["java"])
    for p in process:
        print(p)
