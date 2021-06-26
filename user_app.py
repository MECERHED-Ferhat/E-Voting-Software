import json, constants
from _connection_user_app import sender, fetch

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



def send_vote():
	"""
	res = {
		"request" : "AUTH",
		"elec" : { 
			"nom" : "Djabri",
			"prenom" : "Abdelkader",
			"id" : "FE68126F0C93B5170D",
			"hpin" : "9B031193A1"
		}
	}
	"""
	with open("Vote.json", "rb") as f:
		data = json.loads(f.read().decode("utf-8"))
	sender({
		"src": constants.USER_APP,
		"dest": constants.REGISTER,
		"body": {
			"request": "VERIFY_AUTH",
			"data": data
		},
		"to_string": "Send data"
		})
	return fetch()

def send_vote_server():
	with open("Vote.json", "rb") as f:
		data = json.loads(f.read().decode("utf-8"))
	sender({
		"src": constants.USER_APP,
		"dest": constants.SERVER,
		"body": {
			"request": "FINAL_VOTE",
			"data": data
		},
		"to_string": "Envoi au serveur"
	})

	return fetch()

if __name__ == "__main__":
	pass