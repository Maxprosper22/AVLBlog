import rsa

(pubkey, privkey) = rsa.newkeys(512)

message = 'Hello Bob!'.encode()

crypto = rsa.encrypt(message, pubkey)
message = rsa.decrypt(crypto, privkey)

print(crypto)
print(message.decode('utf8'))