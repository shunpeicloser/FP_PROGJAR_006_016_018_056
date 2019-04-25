import socket

# general purpose socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 9000))

# read-only socket
ros = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Input Your Name")
name = input("> ")
s.send(name.encode())

while True:
    command = input()
    s.send(command.encode())
    data_recv = s.recv(1024)
    print(data_recv.decode())
    if command == 'quit':
        break


s.close()