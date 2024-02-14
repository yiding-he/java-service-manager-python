import sys

from commands.list import list_command
from commands.start import start_command
from commands.stop import stop_command
from domain.config import Config

if __name__ == '__main__':
    Config.init_logging()
    Config.load_config()

    if len(sys.argv) < 2:
        print("Usage: jsm <command>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        list_command()
    elif command == "start":
        start_command()
    elif command == "stop":
        stop_command()
    else:
        print("Unknown command: " + command)
