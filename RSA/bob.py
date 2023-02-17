import socket
from os.path import exists
import sys
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto import Random
import base64

host = 'localhost'
port = 8000

key = get_random_bytes(16)
iv = get_random_bytes(16)

#RSA key generate
random_generator = Random.new().read
# rsa
rsa = RSA.generate(1024, random_generator)
#
private_pem = rsa.exportKey()
with open("private.pem", "wb") as f:
    f.write(private_pem)
#
public_pem = rsa.publickey().exportKey()
with open("public.pem", "wb") as f:
    f.write(public_pem)

#RSAencode
def rsaEnc(rsaPublickey, filename):
    enfilename = filename + '.enc'

    fd1 = open(filename, 'r')
    fd2 = open(enfilename, 'wb')
    filecontent = fd1.read()

    rsakey = RSA.importKey(rsaPublickey)
    print(rsakey)
    cipher = Cipher_pkcs1_v1_5.new(rsakey)  # pkcs1_v1_5
    cipher_text = base64.b64encode(cipher.encrypt(filecontent.encode('utf-8')))
    fd2.write(cipher_text)

    fd1.close()
    fd2.close()

    return enfilename

#RSAdecode
def rsaDec(enckey):
    rsakey = RSA.importKey(open("private.pem").read())
    cipher = Cipher_pkcs1_v1_5.new(rsakey)
    print(cipher)  # pkcs1_v1_5
    aesKey = cipher.decrypt(enckey, "    ")

    return aesKey


#encode
def enc(key, iv, filename):
    enfilename = filename + '.enc'

    fd1 = open(filename, 'rb')
    fd2 = open(enfilename, 'wb+')
    filecontent = fd1.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(filecontent, 16))
    fd2.write(ciphertext)

    fd1.close()
    fd2.close()

    return enfilename
#bind
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))

#connect
server_socket.listen()
print("server_1 start")
client_soc, addr = server_socket.accept()
print('connected client addr : ', addr)

#filename rcv
filename = client_soc.recv(1024)
fn = filename.decode()
print("recv filename : ", fn)
data_transferred = 0
if not exists(fn):
    print('no file')
    sys.exit()

#example.txt read
print('\nOriginal File Content:')
with open(fn) as fd:
        print(fd.read())


#key and iv transfer, public key
while True:
    print('send public key')
    client_soc.sendall(public_pem)

    print("revb iv")
    iv = socket.recv(100)

    print('rev rsaEnckey')
    rsaKey = client_soc.recv(1024)
    print(rsaKey)

    keyData = client_soc.recv(100)
    keyMsg = keyData.decode()

    if keyMsg == 'y':
        print("key transfer success")
        break

#symkey decode
rsaSymKey = rsaDec(rsaKey)




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


print('\nDecrypted File Content')
with open(decfile, 'rb') as fd:
    print(fd.read().decode())

print('client close')
socket.close()