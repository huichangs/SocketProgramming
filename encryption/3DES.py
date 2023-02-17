#3DES_CBC
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

class MyDES3_CBC:
    def __init__(self):
        self.key = get_random_bytes(24)
        self.iv = get_random_bytes(8)

    def enc(self, pfile):
        cfile = pfile + '.enc'

        fd1 = open(pfile, 'rb')
        fd2 = open(cfile, 'wb')
        plaintext = fd1.read()

        cipher1 = DES3.new(self.key, DES3.MODE_CBC, self.iv)
        ciphertext = cipher1.encrypt(pad(plaintext, 8))
        fd2.write(ciphertext)

        fd1.close()
        fd2.close()

        return cfile

    def dec(self, cfile):
        pfile = cfile + '.dec'

        fd1 = open(cfile, 'rb')
        ciphertext = fd1.read()

        cipher2 = DES3.new(self.key, DES3.MODE_CBC, self.iv)
        plaintext = unpad(cipher2.decrypt(ciphertext), 8)

        fd2 = open(pfile, 'wb')
        fd2.write(plaintext)
        fd2.close()

        return pfile


def main():
    myfile = 'example.txt'

    print("Original File(%s) Content:" % myfile)
    print(open(myfile).read())
    print('')

    des3 = MyDES3_CBC()

    encfile = des3.enc(myfile)
    print("Encrypted File(%s) Content:" % encfile)
    print(open(encfile, 'rb').read())
    print('')

    decfile = des3.dec(encfile)
    print("Decrypted File(%s) Content:" % decfile)
    print(open(decfile).read())


if __name__ == '__main__':
    main()