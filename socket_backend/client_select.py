import socket
import time
import select
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('10.151.34.154', 9000))

print("INPUT YOUR NAME")
name = input()
sock.send(name.encode())

input_fd = [sys.stdin, sock]

running = 1
try:
    while running:
        inputready, outputready, error = select.select(input_fd, [], [], 0)
        for fd in inputready:
            if fd ==  sys.stdin:
                command = sys.stdin.readline()

                if command.strip('\n') == 'quit':
                    running = 0
                    break

                if command:
                    sock.send(command.strip('\n').encode())
                    response = sock.recv(1024)
                    print(response.decode())
                #else:
                #    data = sock.recv(1024)
                #    print(data.decode())

            elif fd == sock:
                data = sock.recv(1024)
                print(data.decode())
except KeyboardInterrupt:
    pass

sock.close()
