import socket, json
from time import sleep


HOST = "127.0.0.1"
PORT = 4444

def get_data():
	data = []
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		while True:
			try:
				sleep(3)
				s.connect((HOST, PORT))
			except ConnectionRefusedError as e:
				pass
			else:
				break;

		##############################
		res = {
			"request" : "GET_DATA",
		}
		
		s.send(json.dumps(res, indent=2).encode("utf-8"))
		
		data = json.loads(s.recv(4096).decode("utf-8"))
		##############################

	return data

def auth(electeur):
	auth = 0
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		while True:
			try:
				sleep(3)
				s.connect((HOST, PORT))
			except ConnectionRefusedError as e:
				pass
			else:
				break;

		##############################
		"""
		res = {
			"request" : "AUTH",
			"elec" : { 
				"nom" : "Djabri",
				"prenom" : "Abdelkader",
				"id" : "9531AD056C3A785538",
				"hpin" : "2A0B98A180"
			}
		}
		"""
		res = {
			"request" : "AUTH",
			"elec" :  electeur	
		}

		s.send(json.dumps(res, indent=2).encode("utf-8"))

		auth = json.loads(s.recv(4096).decode("utf-8"))


		##############################

	return auth
