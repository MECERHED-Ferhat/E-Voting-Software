import sqlite3, sys, traceback
import json

connexion = sqlite3.connect("../database.db")
curseur = connexion.cursor()

################################
#get vote

with open("test.json", "r") as f:
	vote = json.load(f)

vote_parti = vote["partie"]
vote_candidats = vote["candidats"]


##################################
#get vote_id

#soit: vote_id : auto increment --> current vote == max(id)? 

# c.execute("""
# 	SELECT max(id)
# 	FROM vote
# 	""")
# id_v = int(c.fetchone()[0])
# print(id_v)

#soit: vote_id : num_vote envoyé avec l'ack 
#recevoir vote --> generer num_vote --> envoyer num_vote avec ack et remplir table vote
vote_id = 2

###################################################################
#recuperer id parti

try:
	curseur.execute("""
	SELECT id
	FROM partie
	WHERE nom = ?
 	""", (vote_parti,))

	id_p = curseur.fetchone()[0]


	connexion.commit()
except sqlite3.Error as er:
	print('SQLite error: %s' % (' '.join(er.args)))
	print("Exception class is: ", er.__class__)
	print('SQLite traceback: ')
	exc_type, exc_value, exc_tb = sys.exc_info()
	print(traceback.format_exception(exc_type, exc_value, exc_tb))

#remplir table vote
try:
	curseur.execute("""
	INSERT INTO vote(id, id_partie) VALUES(?,?)
	 """, (vote_id ,int(id_p),))
	
	
	connexion.commit()
except sqlite3.Error as er:
	print('SQLite error: %s' % (' '.join(er.args)))
	print("Exception class is: ", er.__class__)
	print('SQLite traceback: ')
	exc_type, exc_value, exc_tb = sys.exc_info()
	print(traceback.format_exception(exc_type, exc_value, exc_tb))


###################################################################
#remplir table vote_candidat


for i in vote_candidats:
	candidat = i["nom"]
	classement = vote_candidats.index(i) + 1


	try:
		curseur.execute("""
		SELECT id
		FROM candidat
		WHERE prenom = ?
	 	""", (candidat,))
		id_c =  curseur.fetchone()[0]
		
		connexion.commit()
	except sqlite3.Error as er:
		print('SQLite error: %s' % (' '.join(er.args)))
		print("Exception class is: ", er.__class__)
		print('SQLite traceback: ')
		exc_type, exc_value, exc_tb = sys.exc_info()
		print(traceback.format_exception(exc_type, exc_value, exc_tb))



	try:
		curseur.execute("""
		INSERT INTO vote_candidat (id_vote, id_candidat, classement) VALUES(?,?,?)
	 	""", (vote_id, int(id_c), classement,))
		
		connexion.commit()
	except sqlite3.Error as er:
		print('SQLite error: %s' % (' '.join(er.args)))
		print("Exception class is: ", er.__class__)
		print('SQLite traceback: ')
		exc_type, exc_value, exc_tb = sys.exc_info()
		print(traceback.format_exception(exc_type, exc_value, exc_tb))


connexion.close()