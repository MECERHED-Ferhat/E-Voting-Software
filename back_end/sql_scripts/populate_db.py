import sqlite3, sys, traceback, json, random

connexion = sqlite3.connect("../database.db")
curseur = connexion.cursor()

with open("data.json", "r") as f:
	DATA = json.load(f)


def handle_SQL_error(er):
	print('SQLite error: %s' % (' '.join(er.args)))
	print("Exception class is: ", er.__class__)
	print('SQLite traceback: ')
	exc_type, exc_value, exc_tb = sys.exc_info()
	print(traceback.format_exception(exc_type, exc_value, exc_tb))

def random_key_generator(X):
	# Generate a X long key
	char_set = "0123456789ABCDEF"
	return "".join([random.choice(char_set) for _ in range(X)])

def eligible_random_state():
	# 20% of not being able to vote
	return "FALSE" if random.randint(1,5) == 5 else "TRUE"


def populate_electeur(electeurs):
	try:
		sql_query = """
			DELETE FROM Electeur;
		"""
		curseur.execute(sql_query)
		connexion.commit()
		
		for elec in electeurs:
			try:
				sql_params = (
					elec["id"] or random_key_generator(18),				# ID Electeur
					elec["nom"],																	# Nom Electeur
					elec["prenom"],																# Prenom Electeur
					elec["H_PIN"] or random_key_generator(64),		# H_PIN Electeur
					elec["eligible"] or eligible_random_state()		# Eligible Electeur
				)
				sql_query = """
					INSERT INTO Electeur VALUES (?, ?, ?, ?, ?);
				"""
				curseur.execute(sql_query, sql_params)
				connexion.commit()
			except sqlite3.Error as er:
				handle_SQL_error(er)
	except sqlite3.Error as er:
		handle_SQL_error(er)

def populate_partie(parties):
	try:
		sql_query = """
			DELETE FROM Partie;
			DELETE FROM Candidat;
		"""
		curseur.executescript(sql_query)
		connexion.commit()
		
		for i in range(len(parties)):
			try:
				sql_params = (
					i, 																						# ID Partie
					parties[i]["nom"],														# Nom Partie
					parties[i]["image"]														# Image Partie
				)
				sql_query = """
					INSERT INTO Partie VALUES (?, ?, ?);
				"""
				curseur.execute(sql_query, sql_params)

				sql_query = """
				"""

				for j in range(len(parties[i]["candidats"])):
					sql_params = (
						j, 																					# ID Candidat
						parties[i]["candidats"][j]["nom"],					# Nom Candidat
						parties[i]["candidats"][j]["prenom"],				# Prenom Candidat
						parties[i]["candidats"][j]["image"],				# Image Candidat
						parties[i]["candidats"][j]["classement"],		# Classement Candidat
						i 																					# Id Partie_Candidat
					)
					sql_query = """
						INSERT INTO Candidat VALUES (?, ?, ?, ?, ?, ?);
					"""
					curseur.execute(sql_query, sql_params)

				connexion.commit()
			except sqlite3.Error as er:
				handle_SQL_error(er)
	except sqlite3.Error as er:
		handle_SQL_error(er)


populate_electeur(DATA["electeur"])
populate_partie(DATA["partie"])
connexion.close()