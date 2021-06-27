import socket, sqlite3, sys, traceback, json, os, time, threading
from _connection_server import sender, fetch
import constants
from nanoid import generate

def save_vote(vote):
	connexion = sqlite3.connect("database.db")
	curseur = connexion.cursor()

	try:
		token = generate(size=8)
		sql_query = """
			INSERT INTO Vote(id_partie, token) VALUES (?,?);
		"""
		curseur.execute(sql_query, (vote["vote"]["partie"], token))
		
		sql_query = """
			UPDATE Electeur SET Eligible = 'FALSE' WHERE id = ?;
		"""
		curseur.execute(sql_query, (vote["electeur"]["id"],))
			
		connexion.commit()

		for candidat in vote["vote"]["candidats"]:
			classement = vote["vote"]["candidats"].index(candidat) + 1
			try:
				curseur.execute("""
				SELECT max(rowid)
				FROM Vote;
				""")
				id_v = curseur.fetchone()[0]

				curseur.execute("""
				INSERT INTO vote_candidat (id_vote, id_candidat, classement) VALUES(?,?,?)
			 	""", (id_v, candidat, classement,))
				
				connexion.commit()
			except sqlite3.Error as er:
				print('SQLite error: %s' % (' '.join(er.args)))
				print("Exception class is: ", er.__class__)
				print('SQLite traceback: ')
				exc_type, exc_value, exc_tb = sys.exc_info()
				print(traceback.format_exception(exc_type, exc_value, exc_tb))

		sender({
			"src": constants.SERVER,
			"dest": constants.USER_APP,
			"body": token,
			"to_string": """Send token to client
{token} RSA Encryption
"""
		})
		
	except sqlite3.Error as er:
		print('SQLite error: %s' % (' '.join(er.args)))
		print("Exception class is: ", er.__class__)
		print('SQLite traceback: ')
		exc_type, exc_value, exc_tb = sys.exc_info()
		print(traceback.format_exception(exc_type, exc_value, exc_tb))

	

def check_vote(token):
	connexion = sqlite3.connect("database.db")
	curseur = connexion.cursor()
	try:
		sql_query = """
			SELECT count(*) FROM Vote WHERE token = ?;
		"""
		curseur.execute(sql_query, (token,))

		sender({
			"src": constants.SERVER,
			"dest": constants.USER_APP,
			"body": {
				"ok": (curseur.fetchone()[0] != 0)
			},
			"to_string": """
Verification response to client :

{RESULT} RSA Encryption
"""
		})


	except sqlite3.Error as er:
		print('SQLite error: %s' % (' '.join(er.args)))
		print("Exception class is: ", er.__class__)
		print('SQLite traceback: ')
		exc_type, exc_value, exc_tb = sys.exc_info()
		print(traceback.format_exception(exc_type, exc_value, exc_tb))
	connexion.close()

def main_thread():
	while True:
		res = fetch()

		if "request" in res and res["request"] == "FINAL_VOTE":
			save_vote(res["data"])

		if "request" in res and res["request"] == "CHECK_VOTE":
			check_vote(res["data"])


if __name__ == "__main__":
	threading.Thread(target=main_thread, daemon=True).start()

	while True:
		time.sleep(20)