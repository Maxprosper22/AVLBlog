import rsa

def generateKeys():
    (publicKey, privateKey) = rsa.newkeys(1024)
    
    return publicKey, privateKey
        
def loadkeys():
    with open('keys/pubkey.pem', 'rb') as p:
        publicKey = rsa.PublicKey.load_pkcs1(p.read())
        
    with open('keys/privkey.pem', 'rb') as p:
        privateKey = rsa.PrivateKey.load_pkcs1(p.read())
        
    return privateKey, publicKey
    
def encrypt(message, key):
    return rsa.encrypt(message.encode('ascii'), key)
    
def decrypt(ciphertxt, key):
    try:
        return rsa.decrypt(ciphertxt, key).decode('ascii')
    except:
        return False
        
def sign(message, key):
    return rsa.sign(message.encode('ascii'), key, 'SHA-1')
    
def verify(message, signature, key):
    try:
        return rsa.verify(message.encode('ascii'), signature, key) =='SHA-1'
    except:
        return False
        
generateKeys()
publicKey, privateKey = loadkeys()

message = input('Write a message: ')
ciphertext = encrypt(message, publicKey)

signature = sign(message, privateKey)
text = decrypt(ciphertext, privateKey)