import socket
import os
import sys
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64

server_ip = 'localhost'
server_port = 8000

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((server_ip, server_port))

#RSAdecode
def rsaDec(encfilename):
    decfilename = encfilename + '.dec'

    fd1 = open(encfilename, 'rb')
    fd2 = open(decfilename, 'w')
    content = fd1.read()

    rsakey = RSA.importKey(open("private.pem").read())
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    print(cipher)  # pkcs1_v1_5
    text = cipher.decrypt(base64.b64decode(content), "    ")
    fd2.write(text.decode('utf-8'))

    fd1.close()
    fd2.close()

    return decfilename

#RSAencode
def rsaEnc(rsaPublickey, msg):
    message = msg
    rsakey = RSA.importKey(rsaPublickey)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # pkcs1_v1_5
    print(cipher)
    cipher_key = cipher.encrypt(message)
    return cipher_key

# AESdecode
def dec(key, iv, encfilename):
    decfilename = encfilename + '.dec'

    fd1 = open(encfilename, 'rb')
    fd2 = open(decfilename, 'w')
    content = fd1.read()

    aes = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(aes.decrypt(content), 16)
    fd2.write(plaintext.decode())

    fd1.close()
    fd2.close()

    return decfilename

#filename transfer
print('conncection success')
filename = 'example.txt'
socket.sendall(filename.encode('utf-8'))


#public key, sym key, iv
while True:
    print("recv public key")
    publicKey = socket.recv(1024)
    print(publicKey)

    print("iv transfer")
    socket.sendall(iv)


    global rsaEncKey
    rsaEncKey = rsaEnc(publicKey, key)
    print("send rsaEnc key")
    socket.sendall(rsaEncKey)

    print("Did you rcv key, iv? (y)")
    keymsg = input('anw: ')
    if keymsg == 'y':
        socket.sendall(keymsg.encode(encoding='utf-8'))
        break

data = socket.recv(1024)
data_transferred = 0

if not data:
    print('file is not exit')
    sys.exit()

nowdir = os.getcwd()

#file recv
with open(nowdir + "\\" + filename, 'wb') as f:
    try:
        while data:
            f.write(data)
            data_transferred += len(data)
            data = socket.recv(1024)
    except Exception as ex:
        print(ex)
print("file %s receive complete" %(filename))

decfile = dec(iv, filename)

print('\nDecrypted File Content')
with open(decfile, 'rb') as fd:
    print(fd.read().decode())

print('client close')
socket.close()



