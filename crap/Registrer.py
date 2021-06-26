from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from random import SystemRandom
from nanoid import generate # requirment pip install nanoid
from pathlib import Path
import constants
import RSAModule
import binascii
import hashlib
import base64
import socket
import AES #this is our customized module 
import zlib
import time
import sys



#Function to Recieve files from client side
def ReciveFileFromClient(Filename,conn):
    res = {
        "src": constants.REGISTER,
        "dest": constants.USER_APP,
        "body": Filename.name,
        "to_string": description
    }
    sender(res)

#Function to send files to server using sockets 
def SendFileToServer(Filename) :
    # Sending "Filename" to Server
    with open(fetch(), "rb") as f1:
        with open(Filename, "wb") as f2:
            for i in f1:
                f2.write(i)


"""    
    while True:

        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(4096).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input('insert message:')
        conn.send(data.encode())  # send data to the client
"""

    


if __name__ == '__main__':
    #server_program()

    #======== Different paths to used files ================#

    #Path to the Public and Private key
    private_key = Path('PrivateKey.pem')
    public_key = Path('PublicKey.pem')
    #Path to the file we're willing to encrypt
    unencrypted_Vote = Path('Vote.txt')
    #Path to the signature  
    sigfile = Path("Signature")
    #Path to blided file
    Blindfile=Path("Blind.txt")
    #Path to recieve the blinded file
    RecBlindFile=Path("Blind_Recieved.txt")
    #Recieved Signature decrypted
    RecSignature=Path("Signature_Blind.txt")
    #Write the new signature to a file 
    RegSig=Path('Registrer_signature.txt')
    #File tp send 
    SendingFile=Path("Signature_Request.dat")
    #File to write in the recieved Encrypted file 
    EncBlindFile=Path("Blinded_encrypted.dat")
    #path to the encrypted file
    encrypted_Vote = unencrypted_Vote.with_suffix('.dat')
    #import the rsa key in a public key format 
    PublicKey = RSA.importKey(public_key.read_bytes())




#================================================= Recieve file from Client Side ======================================================#

    ReciveFileFromClient(Filename)

    time.sleep(5)

    conn.close()  # close the connection

    

#============================================== Verify the signature =======================================================#


    #Recieve the file encrypted 
    ReciveFileFromClient(EncBlindFile)
    print("EncBlindFile Recieved \n")
    time.sleep(3)

    #Recieve the Blind file
    ReciveFileFromClient(RecBlindFile)
    print("BlindFile Recieved \n")
    time.sleep(3)


	#========================= Decrypt the file ==========================================#	

	#Read the content of the encrypted file
    with open(EncBlindFile, 'r') as e:
        encrypted_blind = e.read()

    #Decrypt the file 
    decrypted_msg = RSAModule.FileDecryption(encrypted_blind.encode(), private_key.read_bytes())

    #Write the obtained decrypted blid to file 
    with open(RecSignature, 'w') as f:
        f.write(decrypted_msg.decode())

    #=========================== Verify the signature =====================================#

    verification = RSAModule.Verify_File(public_key, RecBlindFile, RecSignature)

    #Drop the communication (close the socket and reopen a new one)
    if(verification is False):
        print("this signature is not valid. \n Closing connection ...")
        sys.exit(-1)



#======================================== Check informations ================================================================#

    #TODO: verifier l'utilisateur dans la base de donnée et vérifier s'il est apte à voter
    print(" [*] Cet utilisateur est pret a voter ")

    #=========================== Accorder à l'utilisateur une signature à utiliser ============================#



    #signing a file
    Signature_registrer= RSAModule.Sign_File(private_key, RecBlindFile)

    #Write Result of sginature to file 
    with open(RegSig, 'w') as f:
        f.write(Signature_registrer.decode())

    #======================= Encrypt the signature with rsa =======================#

    #Encryption function
    encrypted_signature = RSAModule.FileEncryption(regSig.read_bytes(), public_key.read_bytes())
    #Write Result of encryption to file 
    with open(SendingFile, 'w') as f:
        f.write(encrypted_signature.decode())


    #============================================ Send file to Registrer ===========================================================#


    # TODO: INSERT HERE ROUTING CODE TO SEND THE FILE 'SENDINGFILE' AND 'BLINDFILE'

    SendFileToServer(SendingFile, "Sending to Register")
    time.sleep(3)
 

