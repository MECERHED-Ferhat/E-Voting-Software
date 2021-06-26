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
import hashlib
import base64
import socket
import AES #this is our customized module 
import zlib
import time
import sys




#======== Different paths of used files  ================#
private_key = Path('PrivateKey.pem')
public_key = Path('PublicKey.pem')
RecivedFile_from_Client=Path('SignedEncVote.dat')
RecSignedVote=Path('DecrytedSignature.txt')
UnsignedVote = Path('Vote.dat')





if __name__ == '__main__':

#================================================= Recieve file from Client Side =======================================================#


    #TODO: Routage recieve files from client "RecivedFile_from_Client" and 


    #=============================== File Decryption with RSA ====================#

    decryted_Rsa = RSAModule.FileDecryption(RecivedFile_from_Client.read_bytes(), private_key.read_bytes())
    
       #Write Result of sginature to file 
    with open(RecSignedVote, 'w') as f:
        f.write(decryted_Rsa.decode())

    #=============================== Verifing the Signature ========================#

    verifing_signature = RSAModule.Verify_File_Server(private_key,UnsignedVote,RecSignedVote)
    print(verifing_signature)

    #============================== Generate Token ================================#
    #verfy if signature is valid 
    if verifing_signature is True:
        token = RSAModule.Generate_Token()
        vote={token,decryted_Rsa}
        print(vote)
        #================== stoke the dictionary 'vote' in BD ====================#




        #================== Send Token to client ====================#




        #================== recive the private key ====================#




        #==================   calculate the votes  ====================#