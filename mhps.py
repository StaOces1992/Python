#/usr/bin/python

import argparse
import socket
import threading
from queue import Queue

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--target', required=True, help='Target to scan')
parser.add_argument('-ps', '--port_start', default=1, help='Starting port')
parser.add_argument('-pe', '--port_end', default=65535, help='Ending port')
arguments = parser.parse_args()

print_lock = threading.Lock()
OPEN_PORTS = 0

TARGET = socket.gethostbyname(arguments.target)
PORT_START = arguments.port_start
PORT_END = arguments.port_end

print('----------------------------------------------\n')
print('WELCOME TO THE MHACKERS PORT SCANNER !\n')
print('----------------------------------------------\n')
print('Scanning: ' + str(TARGET) + ' from port: ' + str(PORT_START) + ' to port: ' + str(PORT_END) + '\n')
print('----------------------------------------------\n')

def Scan(Port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.settimeout(0.5)
        connection = s.connect((TARGET, Port))
        with print_lock:
            print('Port',Port,'is open!')
        connection.close()
    except:
        pass

def threader():
    while True:
        scanner = q.get()
        Scan(scanner)
        q.task_done()

q = Queue()

for x in range(60):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for scanner in range(int(PORT_START), int(PORT_END)):
    q.put(scanner)

q.join()

print('\n----------------------------------------------\n')
print('Scanning finished !! \n')
print('----------------------------------------------\n')

