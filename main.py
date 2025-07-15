from parser.log_parser import parse_log_file
from parser.live_reader import start_live_uart
from gui.app import launch_app

if __name__ == "__main__":
    launch_app(parse_log_file, start_live_uart)