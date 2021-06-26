from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from random import SystemRandom
from pathlib import Path
import random
import array
import os, sys

#AES file Encryption 
def AESEncryption(key, filename):
	chunksize = 64*1024
	outputFile = filename.with_suffix('.dat')
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = Random.new().read(16)

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:#rb means read in binary
		with open(outputFile, 'wb') as outfile:#wb means write in the binary mode
			outfile.write(filesize.encode('utf-8'))
			outfile.write(IV)

			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break
				elif len(chunk)%16 != 0:
					chunk += b' '*(16-(len(chunk)%16))

				outfile.write(encryptor.encrypt(chunk))

#AES file decryption
def AESDecryption(key, filename):
	chunksize = 64*1024
	outputFile = filename[11:]

	with open(filename, 'rb') as infile:
		filesize = int(infile.read(16))
		IV = infile.read(16)

		decryptor= AES.new(key, AES.MODE_CBC, IV)

		with open(outputFile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))

			outfile.truncate(filesize)

def getKey(password):
	hasher = SHA256.new(password.encode('utf-8'))
	return hasher.digest()

#Generate password of maximum length equal to 12
def GeneratePassword():
 
	# maximum length of password needed
	# this can be changed to suit your password length
	MAX_LEN = 12
 
	# declare arrays of the character that we need in out password
	# Represented as chars to enable easy string concatenation
	DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
	LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    	                 'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
        	             'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
            	         'z']
 
	UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
    	                 'I', 'J', 'K', 'M', 'N', 'O', 'p', 'Q',
        	             'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
            	         'Z']
 
	SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>','*', '(', ')', '<']
 
	# combines all the character arrays above to form one array
	COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
 
	# randomly select at least one character from each character set above
	rand_digit = random.choice(DIGITS)
	rand_upper = random.choice(UPCASE_CHARACTERS)
	rand_lower = random.choice(LOCASE_CHARACTERS)
	rand_symbol = random.choice(SYMBOLS)

	# combine the character randomly selected above
	# at this stage, the password contains only 4 characters but
	# we want a 12-character password
	temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
 
 
	# now that we are sure we have at least one character from each
	# set of characters, we fill the rest of
	# the password length by selecting randomly from the combined
	# list of character above.
	for x in range(MAX_LEN - 4):
		temp_pass = temp_pass + random.choice(COMBINED_LIST)
 
	    # convert temporary password into array and shuffle to
    	# prevent it from having a consistent pattern
    	# where the beginning of the password is predictable
		temp_pass_list = array.array('u', temp_pass)
		random.shuffle(temp_pass_list)
 
	# traverse the temporary password array and append the chars
	# to form the password
	password = ""
	for x in temp_pass_list:
		password = password + x
	with open('password.txt', 'w') as outfile:#wb means write in the binary mode
		outfile.write(password)     
	# print out password
	return password


def Main():
	
	# Signing authority (SA) key
	priv = RSA.generate(2048)
	pub = priv.publickey()

	choice = input("Would you like to (E)encrypt or (D)Decrypt ")

	if choice == 'E':

		filename = input("File to encrypt: ")
		password = GeneratePassword()
		AESEncryption(getKey(password), Path(filename))


		# Generating a random number R the blinding factory
		r = SystemRandom().randrange(pub.n >> 10, pub.n)

		messagefile='(enc)Vote.txt'
		with open(messagefile, 'rb') as m:
			message = m.read()

		messageBlinded = pub.blind(message, r)
		print("\n\n blided:" +str(messageBlinded))
		print('Done.')

	elif choice == 'D':
		filename = input("File to decrypt: ")
		password = input("Password: ")
		AESDecryption(getKey(password), Path(filename))
		print("Done.")

	else:
		print("No option selected, closing...")
	
	

# Main()