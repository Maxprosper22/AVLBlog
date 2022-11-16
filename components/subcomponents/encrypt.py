import bcrypt

def encrypt_pwd(pwd):
    p_word = pwd.encode('utf-8')
    my_hash = bcrypt.hashpw(p_word, bcrypt.gensalt())
    return my_hash
    
def verify(pwd):
    encode_pwd = pwd.encode('utf-8')
    # check = bcrypt.checkpw(encode_pwd, )
    return encode_pwd