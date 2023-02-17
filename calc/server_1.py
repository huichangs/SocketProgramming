#server
import socket, time

host = 'localhost'
port = 3000
amServerPort = 4000
mdServerPort = 5000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))

amcalc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
amcalc_socket.connect((host, amServerPort))

mdcalc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mdcalc_socket.connect((host, mdServerPort))

server_socket.listen()

print("server_1 start")

client_soc, addr = server_socket.accept()

print('connected client addr : ', addr)

while True:
    data = client_soc.recv(100)
    msg = data.decode()
    print('recv msg : ', msg)

    stack = []
    temp = ''

    if msg != 'end':
        for m in msg:
            if m.isdigit():
                stack.append(m)
            else:
                temp += stack.pop() + ','
                temp += stack.pop() + ','
                if m == '+':
                    temp += '+'
                    amcalc_socket.sendall(temp.encode('utf-8'))
                    data2 = amcalc_socket.recv(100)
                    msg2 = data2.decode()
                    stack.append(msg2)
                    print('+ result from amserver : ', msg2)
                    temp = ''
                elif m == '-':
                    temp += '-'
                    amcalc_socket.sendall(temp.encode('utf-8'))
                    data2 = amcalc_socket.recv(100)
                    msg2 = data2.decode()
                    stack.append(msg2)
                    print('- result from amserver : ', msg2)
                    temp = ''
                elif m == '*':
                    temp += '*'
                    mdcalc_socket.sendall(temp.encode('utf-8'))
                    data2 = mdcalc_socket.recv(100)
                    msg2 = data2.decode()
                    stack.append(msg2)
                    print('* result from mdserver: ', msg2)
                    temp = ''
                elif m == '/':
                    temp += '/'
                    mdcalc_socket.sendall(temp.encode('utf-8'))
                    data2 = mdcalc_socket.recv(100)
                    msg2 = data2.decode()
                    stack.append(msg2)
                    print('/ result from mdserver: ', msg2)
                    temp = ''

        msg = stack.pop()
        print('result : ', msg)

    print('recieve msg from amserver : ', msg)
    client_soc.sendall(msg.encode(encoding='utf-8'))


    if msg == 'end':
        amcalc_socket.sendall(msg.encode(encoding='utf-8'))
        mdcalc_socket.sendall(msg.encode(encoding='utf-8'))
        break

time.sleep(3)
print('server close')
amcalc_socket.close()
mdcalc_socket.close()
server_socket.close()







