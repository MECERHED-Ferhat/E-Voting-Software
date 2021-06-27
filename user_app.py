import json, constants
from _connection_user_app import sender, fetch

def get_data():
	res = {
		"src" : constants.USER_APP,
		"dest" : constants.REGISTER,
		"body" : {
			"request" : "GET_DATA"
		},
		"to_string" : """Demande des listes des parties et candidats
de la base de donnée centrale."""
	}
	sender(res)
	data = fetch()
	return data

def check_vote(token):
	sender({
		"src": constants.USER_APP,
		"dest": constants.SERVER,
		"body": {
			"request": "CHECK_VOTE",
			"data": token
		},
		"to_string": """Check counted vote :

{token} RSA Encryption
"""
	})

	return fetch()

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
		"to_string": """Request Authentication :

{
  {
    Authentication,
    {
      {Vote} AES Encryption
    } Blind
  } Signature
} RSA Encryption
"""
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
		"to_string": """Send unblinded signed vote :

{
  {
    {vote} AES Encryption
  } Signature
} RSA Encryption
"""
	})

	return fetch()

def send_key():
	sender({
		"src": constants.USER_APP,
		"dest": constants.SERVER,
		"body": {
			"request": "SEND_KEY",
			"data": None
		},
		"to_string": """
Send AES keys and token to decrypt votes : 

{
  token,
  AES_key
} RSA Encryption
"""
	})

if __name__ == "__main__":
	pass