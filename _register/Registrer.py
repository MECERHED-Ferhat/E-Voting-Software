from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from random import SystemRandom
from nanoid import generate # requirment pip install nanoid
from pathlib import Path
main_dir, _ = os.path.split(os.path.abspath(os.getcwd()))
sys.path.append(main_dir)
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

    #Recieve data and write them to files 
    file = open(Filename, "wb") 
    RecvData = conn.recv(1024)
    while RecvData:
        file.write(RecvData)
        RecvData = conn.recv(1024)
    # Close the file opened at server side once copy is completed
    file.close()

#Function to send files to server using sockets 
def SendFileToServer(client_socket,Filename) :  

    # Sending "Filename" to Server 
    file = open(Filename, "rb")

    SendData = file.read(1024)
    while SendData:
        #Now send the content of "Filename" to server
        client_socket.send(SendData)
        SendData = file.read(1024)    


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
    path_to_buffers = os.path.join(main_dir, "buffers")

    #Path to the Public and Private key
    private_key = Path(os.path.join(path_to_buffers,'PrivateKey.pem'))
    public_key = Path(os.path.join(path_to_buffers,'PublicKey.pem'))
    #Path to the file we're willing to encrypt
    unencrypted_Vote = Path(os.path.join(path_to_buffers,'Vote.txt'))
    #Path to the signature  
    sigfile = Path("Signature")
    #Path to blided file
    Blindfile=Path(os.path.join(path_to_buffers,"Blind.txt"))
    #Path to recieve the blinded file
    RecBlindFile=Path(os.path.join(path_to_buffers,"Blind_Recieved.txt"))
    #Recieved Signature decrypted
    RecSignature=Path(os.path.join(path_to_buffers,"Signature_Blind.txt"))
    #Write the new signature to a file 
    RegSig=Path(os.path.join(path_to_buffers,'Registrer_signature.txt'))
    #File tp send 
    SendingFile=Path(os.path.join(path_to_buffers,"Signature_Request.dat"))
    #File to write in the recieved Encrypted file 
    EncBlindFile=Path(os.path.join(path_to_buffers,"Blinded_encrypted.dat"))
    #path to the encrypted file
    encrypted_Vote = unencrypted_Vote.with_suffix('.dat')
    #import the rsa key in a public key format 
    PublicKey = RSA.importKey(public_key.read_bytes())
    #File to receive from client
    Filename = Path(os.path.join(path_to_buffers,"Recieve.txt"))



    
#====================================== Initiating the Socket connection with the user    =============================================#
    #Get the hostname
    host = socket.gethostname()
    port = 6000  # initiate port no above 1024

    #Get instance
    server_socket = socket.socket()  
    #The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    #Configure how many client the server can listen simultaneously
    server_socket.listen(2)
    print("[*] Waiting for connection")
    time.sleep(5)

    #Accept connection from Client
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))

#================================================= Recieve file from Client Side ======================================================#

    ReciveFileFromClient(Filename,conn)

    time.sleep(5)

    conn.close()  # close the connection

    

#============================================== Verify the signature =======================================================#


    #Recieve the file encrypted 
    ReciveFileFromClient(EncBlindFile,conn)
    print("EncBlindFile Recieved \n")
    time.sleep(3)

    #Recieve the Blind file
    ReciveFileFromClient(RecBlindFile,conn)
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

    SendFileToServer(client_socket,SendingFile)
    time.sleep(3)
 

