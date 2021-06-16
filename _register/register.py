import socket, sqlite3, sys, traceback, json, os, time, threading
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


def auth():
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
		"to_string" : "Database informations"
	}


def main_thread(HOST):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		while True:
			while True:
				try:
					time.sleep(1)
					s.connect((HOST, constants.USER_APP_PORT))
				except Exception:
					continue
				else:
					break;

			while True:
				try:
					data = s.recv(4096)
				except Exception:
					break;
				if not data:
					break
				res = json.loads(data.decode("utf-8"))

				##############################
				if "request" in res["body"] and res["body"]["request"] == "GET_DATA":
					s.send(json.dumps(get_data(), indent=2).encode("utf-8"))

				if "request" in res["body"] and res["body"]["request"] == "AUTH":
					s.send(json.dumps(auth(), indent=2).encode("utf-8"))
	 			##############################

if __name__ == "__main__":
	HOST = "127.0.0.1"

	threading.Thread(target=main_thread, args=(HOST,), daemon=True).start()

	while True:
		time.sleep(20)