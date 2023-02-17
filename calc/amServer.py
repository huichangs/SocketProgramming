#plus minus server
import socket

host = 'localhost'
port = 4000

amserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
amserver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
amserver_socket.bind((host, port))

amserver_socket.listen()

print('amserver start')

server_1, addr = amserver_socket.accept()

print('connected server_1 addr', addr)

while True:
    data = server_1.recv(100)
    msg = data.decode()


    print('recv msg from server_1 : ', msg)

    if msg != 'end':
        stack = []
        temp = msg.split(',')
        num1 = int(temp[0])
        num2 = int(temp[1])
        if temp[2] == '+':
            nummsg = num2 + num1
        elif temp[2] == '-':
            nummsg = num2 - num1

        msg = str(nummsg)

    print('send completed calc to server_1 : ', msg)
    server_1.sendall(msg.encode(encoding='utf-8'))

    if msg == 'end':
        break

print("amServer close")
amserver_socket.close()
