import socket, json, os, sys, time
main_dir, _ = os.path.split(os.path.abspath(os.getcwd()))
sys.path.append(main_dir)
import constants


HOST = "127.0.0.1"

def get_data():
	data = []
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		while True:
			try:
				time.sleep(1)
				s.connect((HOST, constants.USER_APP_PORT))
			except ConnectionRefusedError as e:
				pass
			else:
				break;

		##############################
		res = {
			"src" : constants.USER_APP,
			"dest" : constants.REGISTER,
			"request" : "GET_DATA",
			"to_string" : "Demande des données"
		}
		
		s.send(json.dumps(res, indent=2).encode("utf-8"))
		
		# data = json.loads(s.recv(4096).decode("utf-8"))
		data = []
		##############################

	return data

def auth(electeur):
	auth = 0
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		while True:
			try:
				time.sleep(1)
				s.connect((HOST, constants.USER_APP_PORT))
			except Exception:
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
			"src" : constants.USER_APP,
			"dest" : constants.REGISTER,
			"body" : {	
				"request" : "AUTH",
				"elec" :  electeur
			},
			"to_string" : "Authentification"
		}

		s.send(json.dumps(res, indent=2).encode("utf-8"))

		# auth = json.loads(s.recv(4096).decode("utf-8"))
		auth = {}

		##############################

	return auth