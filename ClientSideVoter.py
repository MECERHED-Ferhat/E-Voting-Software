import sys, os
import constants
from _connection_user_app import sender, fetch

#Function to send files to server using sockets 
def SendFileToServer(client_socket,Filename) :  

	# Sending "Filename" to Server 
	file = open(Filename, "rb")

	SendData = file.read(1024)
	while SendData:
		#Now send the content of "Filename" to server
		client_socket.send(SendData)
		SendData = file.read(1024) 

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

"""
	message = input("insert message:")  # take input

	while message.lower().strip() != 'bye':
		client_socket.send(message.encode())  # send message
		data = client_socket.recv(1024).decode()  # receive response

		print('Received from server: ' + data)  # show in terminal

		message = input("insert message:")  # again take input

	client_socket.close()  # close the connection
"""

def get_data():
	res = {
		"src" : constants.USER_APP,
		"dest" : constants.REGISTER,
		"body" : {
			"request" : "GET_DATA"
		},
		"to_string" : "Demande des données"
	}
	sender(res)
	data = fetch()
	return data

def auth(electeur):
	##############################
	"""
	res = {
		"request" : "AUTH",
		"elec" : { 
			"nom" : "Djabri",
			"prenom" : "Abdelkader",
			"id" : "4B9CDBC3DB254A4D63",
			"hpin" : "533758A816"
		}
	}
	"""
	res = {
		"src" : constants.USER_APP,
		"dest" : constants.REGISTER,
		"body" : {	
			"request" : "AUTH",
			"elec" :  electeur
		},
		"to_string" : "Authentification"
	}

	sender(res)
	auth = fetch()
	return auth


if __name__ == '__main__':
	from cryptography.hazmat.primitives import serialization, hashes
	from cryptography.hazmat.primitives.asymmetric import padding
	from cryptography.hazmat.backends import default_backend
	from cryptography.exceptions import InvalidSignature
	from Crypto.Cipher import PKCS1_OAEP
	from Crypto.PublicKey import RSA
	from random import SystemRandom
	from nanoid import generate # requirment pip install nanoid
	from pathlib import Path
	import RSAModule
	import hashlib
	import base64
	import socket
	import AES #this is our customized module 
	import zlib
	import time
	#client_program()


#================ Key Generation ==================#


	# Generate_new_key_pair() this function is executed in the dedicated governement page for vote that takes in charge the key distribution
	RSAModule.generate_new_key_pair()

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
	#Write the new signature to a file 
	RegSig=Path('Registrer_signature.txt')
	#The final signed vote blinded
	SignedBlindedVote=Path("SignedBlindedVote.txt")
	#The unblinded signed vote
	SignedUnBlindedVote=Path("SignedUnBlindedVote.txt")
	#The final signed vote
	SignedVote=Path("SignedVote.txt")
	#File tp send 
	SendingFile=Path("Signature_Request.dat")
	#path to the encrypted file
	encrypted_Vote = unencrypted_Vote.with_suffix('.dat')
	#import the rsa key in a public key format 
	PublicKey = RSA.importKey(public_key.read_bytes())
	#the Registrer signature
	Signature_Response=Path("Registrer_signature.txt")
	#File to write in the recieved Encrypted file 
	EncBlindFile=Path("Blinded_encrypted.dat")
	SendingFile_server=Path('SignedEncVote.dat')



	
#====================================== Initiating the Socket connection with the server    ============================================#
	
	# Since both codes are running on the same pc
	host = socket.gethostname()  
	port = 6000  # socket server port number

	# instantiate the connection to the server
	client_socket = socket.socket()  
	client_socket.connect((host, port))  # connect to the server

#========================================= User Authentication with registration =======================================================#
	
	with open("__vote_user_app__.dat", "rb") as f:
		user_info = json.loads(f)
	with open("__vote_user_app__.dat", "wb") as f:
		pass
	print(user_info)

#========================================== Prepare vote before sending it to register =================================================#

	#==================== Encrypting the vote using the AESmodule ==================# 

	#Generate a random password that will be used within the AES
	password = AES.GeneratePassword()

	AES.AESEncryption(AES.getKey(password), unencrypted_Vote)

	# Generating a random number R the blinding factory
	r = SystemRandom().randrange(PublicKey.n >> 10, PublicKey.n)

	with open(encrypted_Vote, 'rb') as m:
		message = m.read()

	#======================= Blinding the encrypted vote =========================#
	VoteBlinded  = PublicKey.blind(message, r)

	with open(Blindfile, 'w') as outfile:#wb means write in the binary mode
		outfile.write(str(VoteBlinded))

	#print("\n\n blided:" +str(VoteBlinded ))
	#print('Done.')

	#======================= Sign the Blinded file ================================# 

	#signing a file
	Signature=RSAModule.Sign_File(private_key, Blindfile)

	#Write Result of sginature to file 
	with open(sigfile, 'w') as f:
		f.write(Signature.decode())

	#======================= Encrypt the signature with rsa =======================#

	#Encryption function
	encrypted_signature = RSAModule.FileEncryption(sigfile.read_bytes(), public_key.read_bytes())
	#Write Result of encryption to file 
	with open(SendingFile, 'w') as f:
		f.write(encrypted_signature.decode())

	print('Done.')

#============================================ Send file to Registrer ===========================================================#


			#INSERT HERE ROUTING CODE TO SEND THE FILE 'SENDINGFILE' AND 'BLINDFILE'

	
	SendFileToServer(client_socket,SendingFile)
	print('file 1 sent')
	time.sleep(3)
	SendFileToServer(client_socket,Blindfile)
	print('File 2 sent')
	time.sleep(10)    
	
#========================================= Receive the new signature from registrer ==============================================#

	
	#Recieve the file encrypted 
	ReciveFileFromClient(EncBlindFile,conn)
	time.sleep(3)
	

	#======================= Decrypt the signature with rsa =======================#


	#Decrypt the file 
	decrypted_msg = RSAModule.FileDecryption(EncryptedBlindFile.encode(), private_key.read_bytes())

	#Write the obtained decrypted blind to file 
	with open(SignedBlindedVote, 'w') as f:
		f.write(decrypted_msg.decode())

	#======================= Unblind the Received file ======================================#

	messageSignature = PublicKey.unblind(SignedBlindedVote[0], r)
	print("\n\n unblind" +str(messageSignature))

	#Write the unblinded vote to file 
	with open(SignedUnBlindedVote, 'w') as f:
		f.write(messageSignature.decode())


#================================ Prepare Files to send to the server side ===============================================#

	#=================== Encrypt the signature with rsa ====================#
	
	encrypted_signature_server = RSAModule.FileEncryption(SignedUnBlindedVote.read_bytes(), public_key.read_bytes())

	#Write Result of encryption to file 
	with open(SendingFile_server, 'w') as f:
		f.write(encrypted_signature_server.decode())

		 #======================= send the encrypted signed vote to server =======================#





		#======================= recieve the token from server =======================#





		#======================= send the private key to server at 20:00 =======================#


	day_and_time_end_of_vote = "24/06/2021 20:00"
	now = datetime.now()
	dt_string = str(now.strftime("%d/%m/%Y %H:%M"))
	today = str(date.today())
	#verfy if it is the time to send the private key to server 
	if dt_string == day_and_time_end_of_vote :
		print("send private key")
		#================== send the private key====================#
