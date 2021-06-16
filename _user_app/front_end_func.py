import socket, json, os, sys, time
from _connection import sender, fetch
main_dir, _ = os.path.split(os.path.abspath(os.getcwd()))
sys.path.append(main_dir)
import constants


HOST = "127.0.0.1"

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

	sender(res)

	auth = fetch()
	##############################

	return auth