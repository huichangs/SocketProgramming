from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
import base64

#
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

message = "Hello,This is RSA  "
rsakey = RSA.importKey(open("public.pem").read())
print(rsakey)
cipher = Cipher_pkcs1_v1_5.new(rsakey)#      pkcs1_v1_5
print(cipher)
cipher_text = base64.b64encode(cipher.encrypt(message.encode('utf-8')))
print(cipher_text.decode('utf-8'))


rsakey = RSA.importKey(open("private.pem").read())
print(rsakey)
cipher = Cipher_pkcs1_v1_5.new(rsakey)
print(cipher)#      pkcs1_v1_5
text = cipher.decrypt(base64.b64decode(cipher_text), "    ")
print(text.decode('utf-8'))