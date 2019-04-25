import socket
import time
import select
import sys
import threading

def threadTest(challenger):
    print('You are challenged by', challenger, ', accept? [Y/n]')
    msg = input()
    print('the msg', msg)
    return

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

                if command:
                    sock.send(command.strip('\n').encode())
                    response = sock.recv(1024)
                    print(response.decode())

                    if command.strip('\n') == 'quit':
                        running = 0
                        break
                #else:
                #    data = sock.recv(1024)
                #    print(data.decode())

            elif fd == sock:
                data = sock.recv(1024)
                alert = data.decode().split()
                print(data.decode())
                if alert[0] == 'challenge' and alert[1] == 'invite':
                    a = threading.Thread(target = threadTest)
                    a.start()
                    a.join()
except KeyboardInterrupt:
    pass

sock.close()
