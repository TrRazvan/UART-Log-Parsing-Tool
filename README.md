# UART Log Parser Tool
GUI application for reading and viewing UART logs from files or live capture from the serial port.
A simple Python tool to parse and export UART log files into CSV format.  
Useful for embedded developers and testers.

## Features
- Parse UART log file with timestamp, direction (RX/TX), message and delay
- Live capture of UART from serial port with configurable parameters (baudrate, duration)
- Table view with column sorting
- Error message coloring (red) and warning (yellow)
- Automatic CSV saving with processed data

## Usage
- Install application requirements using `pip install -r requirements.txt` command
- Run application with `python main.py` command