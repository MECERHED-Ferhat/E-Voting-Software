from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from pathlib import Path
import base64
import zlib
from nanoid import generate
import sys, os
import hashlib
import base64
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

# Function to generate new key pair
def generate_new_key_pair():
    #Generate a public/ private key pair using 4096 bits key length (512 bytes)
    new_key = RSA.generate(4096, e=65537)

    #The private key in PEM format
    private_key = new_key.exportKey("PEM")

    #The public key in PEM Format
    public_key = new_key.publickey().exportKey("PEM")

    private_key_path = Path('PrivateKey.pem')
    private_key_path.touch(mode=0o600)
    private_key_path.write_bytes(private_key)

    public_key_path = Path('PublicKey.pem')
    public_key_path.touch(mode=0o664)
    public_key_path.write_bytes(public_key)


#Our Encryption Function
def FileEncryption(blob, public_key):
    #Import the Public Key and use for encryption using PKCS1_OAEP
    rsa_key = RSA.importKey(public_key)
    rsa_key = PKCS1_OAEP.new(rsa_key)

    #compress the data first
    blob = zlib.compress(blob)
    #In determining the chunk size, determine the private key length used in bytes
    #and subtract 42 bytes (when using PKCS1_OAEP). The data will be in encrypted
    #in chunks
    chunk_size = 470
    offset = 0
    end_loop = False
    encrypted = bytearray()

    while not end_loop:
        #The chunk
        chunk = blob[offset:offset + chunk_size]

        #If the data chunk is less then the chunk size, then we need to add
        #padding with " ". This indicates the we reached the end of the file
        #so we end loop here
        if len(chunk) % chunk_size != 0:
            end_loop = True
            #chunk += b" " * (chunk_size - len(chunk))
            chunk += bytes(chunk_size - len(chunk))
        #Append the encrypted chunk to the overall encrypted file
        encrypted += rsa_key.encrypt(chunk)

        #Increase the offset by chunk size
        offset += chunk_size

    #Base 64 encode the encrypted file
    return base64.b64encode(encrypted)


#Our Decryption Function
def FileDecryption(encrypted_blob, private_key):

    #Import the Private Key and use for decryption using PKCS1_OAEP
    rsakey = RSA.importKey(private_key)
    rsakey = PKCS1_OAEP.new(rsakey)

    #Base 64 decode the data
    encrypted_blob = base64.b64decode(encrypted_blob)

    #In determining the chunk size, determine the private key length used in bytes.
    #The data will be in decrypted in chunks
    chunk_size = 512
    offset = 0
    decrypted = bytearray()

    #keep loop going as long as we have chunks to decrypt
    while offset < len(encrypted_blob):
        #The chunk
        chunk = encrypted_blob[offset: offset + chunk_size]

        #Append the decrypted chunk to the overall decrypted file
        decrypted += rsakey.decrypt(chunk)

        #Increase the offset by chunk size
        offset += chunk_size

    #return the decompressed decrypted data
    return zlib.decompress(decrypted)

#RSA Sign a Message using a private key
def Sign_File(Privatekey_file, messagefile):

    #Open the private key 
    with open(Privatekey_file, 'rb') as f:
        private_key = serialization.load_pem_private_key(f.read(),password=None,backend=default_backend())

    #Read the content of the message and generate hash of the file
    with open(messagefile, 'r') as m:
        message = m.read().encode('ascii')
    prehashed = hashlib.sha256(message).hexdigest()

    #Compare the calculated hash with the obtained signature
    m = open(messagefile,'r')
    sign_message = private_key.sign(bytes(prehashed.encode('ascii')),padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
    
    return base64.b64encode(sign_message)


#RSA Verify a Message against a pubkey
def Verify_File(Publickey_file, messagefile, sigfile):

    #Load the public key from file 
    with open(Publickey_file ,'rb') as f:
        public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())

    #Read the content of the message from file
    with open(messagefile,'rb') as m:
        message = m.read()
    prehashed_msg = hashlib.sha256(message).hexdigest() # generate a hash of the file 


    #Read the content of the signature from file 
    with open(sigfile,'rb') as s:
        sig_message = s.read()
        decoded_sig = base64.b64decode(sig_message)

    try:
        public_key.verify(decoded_sig,bytes(prehashed_msg.encode('ascii')),padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
        print('valid!')

    except InvalidSignature:
        print('invalid!')


#Function that generates a token (to find voters file and check that your vote hasn't been modified) 
def Generate_Token():
# requirment pip install nanoid

    #We limited the size to 8, by this we can generate more then 100 million unique ID 
    return generate(size=8)


#================ Key Generation ==================#

if __name__ == "__main__":
    # Generate_new_key_pair() # run if you don't already have a key pair
    generate_new_key_pair()


    #======== Different paths to files ================#


    #Path to the Public and Private key
    private_key = Path('PrivateKey.pem')
    public_key = Path('PublicKey.pem')
    #Path to the file we're willing to encrypt
    unencrypted_file = Path('Vote.json')
    #Path to the signature  
    sigfile = Path("signature")
    #path to the encrypted file
    encrypted_file = unencrypted_file.with_suffix('.dat')



    #================== Encryption ====================#


    #Encryption function
    encrypted_msg = FileEncryption(unencrypted_file.read_bytes(), public_key.read_bytes())
    #Write Result of encryption to file 
    with open(encrypted_file, 'w') as f:
        f.write(encrypted_msg.decode())



    #================== Decryption ====================#


    #Read the content of the encrypted file
    with open(encrypted_file, 'r') as e:
        encrypted_msg = e.read()

    #Decrypt the file 
    decrypted_msg = FileDecryption(encrypted_msg.encode(), private_key.read_bytes())

    #Write the obtained plain text to file 
    with open('Plaintext.txt', 'w') as f:
        f.write(decrypted_msg.decode())


    #================== Signing a message ====================#

    #signing a file
    Sig=Sign_File(private_key, unencrypted_file )

    #Write Result of sginature to file 
    with open(sigfile, 'w') as f:
        f.write(Sig.decode())


    #================== Verifing a sginature ====================#


    Verify_File(public_key,unencrypted_file ,sigfile)


    #================= Generating a Token =======================#

    #token = Generate_Token()
