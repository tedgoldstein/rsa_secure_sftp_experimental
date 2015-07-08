HOST="medbook.ucsc.edu"
USERNAME="ted"
PASSWORD=""

pubkey ='''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsRUBzf7xjbFFyPDotW9E
AQDtHN5OxfUVnEUt/zcWzupnTzymaVvjlva4MsutqEL4XN9UMymz3IkFV0B08Pp5
FwoANmjq1qIhcEE8RBl7wHsdipGyvbH9igrMFs9d0IxipoQeLIuBlad+g81/Q9jy
PoU5wmtWCNfweeyNJJ3bTnscBvvty3myQbOPLOAGNs6rz8HJo2OwgoY1JPQi17Us
uMaiZ/FSyWHkK3vOkOAY6RMGk+c9Kke8TbNs9crgwhgVy+Gcv2c8nzs1SB6ce7nf
PXndSu8HBWTVIVOhERGgV9b5Ka9Hs5WSvJ8NCJODcRlMS71Nxw4tzVy0knRp6EuH
PwIDAQAB
-----END PUBLIC KEY-----
'''
import sys, os, pdb, os.path

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES,PKCS1_OAEP
random = Random.new()

def encrypt_RSA(message):
    rsakey = RSA.importKey(pubkey)
    rsakey = PKCS1_OAEP.new(rsakey)
    encrypted = rsakey.encrypt(message)
    return encrypted.encode('base64')

import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, username=USERNAME, password=PASSWORD)
sftp = client.open_sftp()

BlockSize = 1048576

def xfer(FILE_NAME):
    input = open(FILE_NAME);
    total = size = os.path.getsize(FILE_NAME);
    output = sftp.open(FILE_NAME, "w")

    # make a one time use key for encrypting this file
    symmetric_key = random.read(32);

    # encrypt the key with the public key above
    output.write(encrypt_RSA(symmetric_key))
    iv = random.read(AES.block_size);
    cipher = AES.AESCipher(symmetric_key, AES.MODE_CFB, iv)
    output.write(iv)

    # Process the input stream

    while True:
        data = input.read(BlockSize);
        total -= len(data);
        if data == '': break # Check for EOF
        output.write(cipher.encrypt(data))
        sys.stderr.write(FILE_NAME+ ": " + format(float(total * 100.0) / float(size), ".2f") + "% remaining\r")

    sys.stderr.write(FILE_NAME+ ": tranferred\n");
    output.close

for top in sys.argv[1:]:
    for comp in top.split("/"):
        if comp == "" or comp == "..":
            sys.stderr.write(comp + "paths which begin with / and paths with .. are prohibited\n")
            sys.exit(1);
    if not os.path.exists(top):
        sys.stderr.write("file name " + top + "does not exist\n")
        sys.exit(1);

    if os.path.isdir(top):
        try:
            sftp.mkdir(top)
        except:
            pass
        for root, dirs, files in os.walk(top):
            for name in dirs:
                try:
                    sftp.mkdir(os.path.join(root, name))
                except:
                    pass
            for name in files:
                FILE_NAME = os.path.join(root, name)
                xfer(FILE_NAME)
    else:
        xfer(top)

client.close()
