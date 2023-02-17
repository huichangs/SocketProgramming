#client
import socket

server_ip = 'localhost'
server_port = 3000

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((server_ip, server_port))

def postfix(expression):
    cal = ''
    stack = []
    for e in expression:
        if e not in'(*/+-)':
            cal += e
        else:
            if e == '(':
                stack.append('(')
            elif e in '*/':
                while stack and stack[-1] in '*/':
                    cal += stack.pop()
                stack.append(e)
            elif e in '+-':
                while stack and stack[-1] != '(':
                    cal += stack.pop()
                stack.append(e)
            elif e == ')':
                while stack and stack[-1] != '(':
                    cal += stack.pop()
                stack.pop()
    while stack:
        cal += stack.pop()
    return cal

while True:
    msg = input('msg : ')
    msg = postfix(msg)
    print('send postfix meg to server : ', msg)
    socket.sendall(msg.encode(encoding='utf-8'))
    data = socket.recv(100)
    msg = data.decode()
    print('result from server : ', msg)

    if msg == 'end':
        break

print('client close')
socket.close()