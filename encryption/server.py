import socket
from os.path import exists
import sys
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

host = 'localhost'
port = 8000

key = get_random_bytes(8)


#encode
def enc(key, filename):
    enfilename = filename + '.enc'

    fd1 = open(filename, 'rb')
    fd2 = open(enfilename, 'wb+')
    filecontent = fd1.read()

    cipher = DES.new(key, DES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(filecontent, 8))
    fd2.write(ciphertext)

    fd1.close()
    fd2.close()

    return enfilename

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))

server_socket.listen()
print("server_1 start")

client_soc, addr = server_socket.accept()
print('connected client addr : ', addr)

filename = client_soc.recv(1024)
fn = filename.decode()
print("recv filename : ", fn)
data_transferred = 0

if not exists(fn):
    print('no file')
    sys.exit()

print('\nOriginal File Content:')
with open(fn) as fd:
        print(fd.read())

#encode
enfile = enc(key, fn)

print('\nEncrypted File Content:')
with open(enfile, 'rb') as fd:
    print(fd.read())

while True:
    print("key transfer")
    client_soc.sendall(key)

    keyData = client_soc.recv(100)
    keyMsg = keyData.decode()

    if keyMsg == 'y':
        print("key transfer success")
        break

#file transfer
print('start file transfer')
with open(enfile, 'rb') as f:
    try:
        data = f.read(1024)
        while data:
            data_transferred += client_soc.send(data)
            data = f.read(1024)
    except Exception as ex:
        print(ex)

print("transfer complete %s, dataAmount %d" %(enfile, data_transferred))

print("server close")
server_socket.close()