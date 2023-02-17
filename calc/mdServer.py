# multiplication division server
import socket

host = 'localhost'
port = 5000

mdserver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mdserver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mdserver_socket.bind((host, port))

mdserver_socket.listen()

print('mdserver start')

server_1, addr = mdserver_socket.accept()

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
        if temp[2] == '*':
            nummsg = num2 * num1
        elif temp[2] == '/':
            nummsg = num2 // num1

        msg = str(nummsg)

    print('send completed calc to server_1 : ', msg)
    server_1.sendall(msg.encode(encoding='utf-8'))

    if msg == 'end':
        break

print("amServer close")
mdserver_socket.close()