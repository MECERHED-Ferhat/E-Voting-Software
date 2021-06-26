import socket, sqlite3, sys, traceback, json, os, time, threading
from _connection import sender, fetch
main_dir, _ = os.path.split(os.path.abspath(os.getcwd()))
sys.path.append(main_dir)
import constants


def get_data():
	connexion = sqlite3.connect("./database.db")
	curseur = connexion.cursor()

	db_data = []
	try:
		sql_query = """
			SELECT * FROM Partie;
		"""
		curseur.execute(sql_query)

		results = curseur.fetchall()
		for result in results:
			db_data.append(dict())
			db_data[-1]["id"] = result[0]
			db_data[-1]["nom"] = result[1]
			db_data[-1]["wilaya"] = result[2]
			db_data[-1]["image"] = result[3]
			db_data[-1]["candidats"] = []
			curseur.execute("""
				SELECT *
				FROM Candidat
				WHERE id_partie = ?
			""", (result[0],))
			list_candidat = curseur.fetchall()
			for cand in list_candidat:
				db_data[-1]["candidats"].append(dict())
				db_data[-1]["candidats"][-1]["id"] = cand[0]
				db_data[-1]["candidats"][-1]["nom"] = cand[1]
				db_data[-1]["candidats"][-1]["prenom"] = cand[2]
				db_data[-1]["candidats"][-1]["image"] = cand[3]
	except sqlite3.Error as er:
		print('SQLite error: %s' % (' '.join(er.args)))
		print("Exception class is: ", er.__class__)
		print('SQLite traceback: ')
		exc_type, exc_value, exc_tb = sys.exc_info()
		print(traceback.format_exception(exc_type, exc_value, exc_tb))
		db_data = []
	connexion.close()
	return {
		"src" : constants.REGISTER,
		"dest" : constants.USER_APP,
		"body" : db_data,
		"to_string" : "Database informations"
	}


def auth(res):
	connexion = sqlite3.connect("./database.db")
	curseur = connexion.cursor()
	auth = {"ok" : False}
	try:
		curseur.execute("""
				SELECT H_PIN, Eligible
				FROM Electeur
				WHERE id = ?
			""", (res["elec"]["id"],))
		results = curseur.fetchone()
		if results is not None: #il existe dans la bdd--> +18 ans et algerien
			if results[0] == res["elec"]["hpin"] and results[1] == "TRUE": #check hpin and eligible
				auth = { "ok" : True}
				print("Access granted")
			else:
				print("Access denied")
		else:
			print("Not Eligible")


	except sqlite3.Error as er:
		print('SQLite error: %s' % (' '.join(er.args)))
		print("Exception class is: ", er.__class__)
		print('SQLite traceback: ')
		exc_type, exc_value, exc_tb = sys.exc_info()
		print(traceback.format_exception(exc_type, exc_value, exc_tb))
		
	connexion.close()
	return {
		"src" : constants.REGISTER,
		"dest" : constants.USER_APP,
		"body" : auth,
		"to_string" : "Authentication check"
	}


def main_thread():
	while True:
		res = fetch()

		if "request" in res and res["request"] == "GET_DATA":
			sender(get_data())

		if "request" in res and res["request"] == "AUTH":
			sender(auth(res))


if __name__ == "__main__":
	threading.Thread(target=main_thread, daemon=True).start()

	while True:
		time.sleep(20)