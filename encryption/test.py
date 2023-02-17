#AES, CBC
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class MyAES_CBC:
    def __init__(self):
        self.key = get_random_bytes(16)
        self.iv = get_random_bytes(16)

    def enc(self, filename):
        encfilename = filename + '.enc'

        fd1 = open(filename, 'rb')
        fd2 = open(encfilename, 'wb+')
        filecontent = fd1.read()

        #AES_CBC로 암호화 한 후 암호화 한 파일을 .enc 파일로 저장
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        ciphertext = cipher.encrypt(pad(filecontent, 16))
        fd2.write(ciphertext)

        # 파일 닫기
        fd1.close()
        fd2.close()

        return encfilename

    def dec(self, encfilename):
        decfilename = encfilename + '.dec'

        fd1 = open(encfilename, 'rb')
        fd2 = open(decfilename, 'w')
        content = fd1.read()

        aes = AES.new(self.key, AES.MODE_CBC, self.iv)
        plaintext = unpad(aes.decrypt(content), 16)
        fd2.write(plaintext.decode())

        fd1.close()
        fd2.close()

        return decfilename



myfile = 'example.txt'

aes = MyAES_CBC()
encfile = aes.enc(myfile)
decfile = aes.dec(encfile)

print('\nOriginal File Content:')
with open(myfile) as fd:
        print(fd.read())

print('\nEncrypted File Content:')
with open(encfile, 'rb') as fd:
    print(fd.read())

print('\nDecrypted File Content')
with open(decfile, 'rb') as fd:
    print(fd.read().decode())


