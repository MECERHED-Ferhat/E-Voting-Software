import sqlite3, sys, traceback
import json, random
from nanoid import generate

connexion = sqlite3.connect("../../database.db")
curseur = connexion.cursor()

################################
#get vote

votes = []

try:
	sql_query = """
	SELECT *
	FROM Electeur;
	"""
	curseur.execute(sql_query)
	list_electeur = curseur.fetchall()

	sql_query = """
	SELECT *
	FROM Partie;
	"""
	curseur.execute(sql_query)
	list_partie = curseur.fetchall()

	sql_query = """
	SELECT *
	FROM Candidat;
	"""
	curseur.execute(sql_query)
	list_candidat = curseur.fetchall()

	for i in range(len(list_partie)):
		if "candidats" not in list_partie[i]:
			list_partie[i] = list(list_partie[i])
			list_partie[i].append(list())
		for j in list_candidat:
			if j[4] == list_partie[i][0]:
				list_partie[i][-1].append(j[0])


	for elec in list_electeur:
		partie = random.choice(list_partie)
		tmp_list = list(partie[-1])
		random.shuffle(tmp_list)

		votes.append({
			"partie": partie[1],
			"candidats": tmp_list
			})

	sql_query = """
	DELETE FROM Vote;
	DELETE FROM Vote_Candidat;
	"""
	curseur.executescript(sql_query)

except sqlite3.Error as er:
	print('SQLite error: %s' % (' '.join(er.args)))
	print("Exception class is: ", er.__class__)
	print('SQLite traceback: ')
	exc_type, exc_value, exc_tb = sys.exc_info()
	print(traceback.format_exception(exc_type, exc_value, exc_tb))

for vote in votes:
	vote_parti = vote["partie"]
	vote_candidats = vote["candidats"]

	###################################################################
	#recuperer id parti

	try:
		curseur.execute("""
		SELECT id
		FROM partie
		WHERE nom = ?
	 	""", (vote_parti,))

		id_p = curseur.fetchone()[0]

		#remplir table vote
		curseur.execute("""
		INSERT INTO Vote(id_partie,token) VALUES(?,?)
		 """, (int(id_p),generate(size=8)))
		
		
		connexion.commit()
	except sqlite3.Error as er:
		print('SQLite error: %s' % (' '.join(er.args)))
		print("Exception class is: ", er.__class__)
		print('SQLite traceback: ')
		exc_type, exc_value, exc_tb = sys.exc_info()
		print(traceback.format_exception(exc_type, exc_value, exc_tb))


	###################################################################
	#remplir table vote_candidat

	for candidat in vote_candidats:
		classement = vote_candidats.index(candidat) + 1

		try:
			curseur.execute("""
			SELECT max(rowid)
			FROM Vote;
			""")
			id_v = curseur.fetchone()[0]
			print(id_v)


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

connexion.close()