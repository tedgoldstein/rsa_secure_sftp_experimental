import sys,pdb

def generate_RSA(bits=2048):
    '''
    Generate an RSA keypair with an exponent of 65537 in PEM format
    param: bits The key length in bits
    Return private key and public key
    '''
    from Crypto.PublicKey import RSA 
    new_key = RSA.generate(bits, e=65537) 
    public_key = new_key.publickey().exportKey("PEM") 
    private_key = new_key.exportKey("PEM") 
    return private_key, public_key


def write(fn, k):
    f = open(fn, "wb");
    f.write(k)
    f.close();


def main():
    privkey,pubkey = generate_RSA();
    write("privkey", privkey);
    write("pubkey", pubkey);

main()
