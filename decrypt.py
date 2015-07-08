import sys,pdb

from Crypto.Cipher import AES, PKCS1_OAEP

def decrypt_RSA(private_key_loc, package):
    '''
    param: public_key_loc Path to your private key
    param: package String to be decrypted
    return decrypted string
    '''
    from Crypto.PublicKey import RSA 
    from Crypto.Cipher import PKCS1_OAEP 
    from base64 import b64decode 
    key = open(private_key_loc, "r").read() 
    rsakey = RSA.importKey(key) 
    rsakey = PKCS1_OAEP.new(rsakey) 
    b = b64decode(package) 
    decrypted = rsakey.decrypt(b);
    return decrypted


input = open("enc");
output = open("dec", "wb");

symkey = decrypt_RSA("privkey", input.read(349));


iv = input.read(AES.block_size)
     
# Create the cipher object and process the input stream
cipher = AES.AESCipher(symkey, AES.MODE_CFB, iv)
method = cipher.decrypt
             
while True:
    data = input.read(AES.block_size)
    if data == '': break # Check for EOF
    output.write(method(data))

output.close();
