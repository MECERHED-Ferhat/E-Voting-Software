import sqlite3, sys, traceback

connexion = sqlite3.connect("../database.db")
curseur = connexion.cursor()

#view for number of votes per party
try:
	sql_query = """
			create view if not exists V(parti, nb_vote) as SELECT nom, count(id_partie) as result
											FROM partie, vote
											WHERE partie.id = vote.id_partie
											GROUP BY vote.id_partie
											ORDER BY result desc
	"""
	curseur.execute(sql_query)


	connexion.commit()
except sqlite3.Error as er:
	print('SQLite error: %s' % (' '.join(er.args)))
	print("Exception class is: ", er.__class__)
	print('SQLite traceback: ')
	exc_type, exc_value, exc_tb = sys.exc_info()
	print(traceback.format_exception(exc_type, exc_value, exc_tb))

#get max value --> winner
try:
	sql_query = """
		SELECT  parti, nb_vote
		FROM V
		WHERE nb_vote = (SELECT max(nb_vote)
						 FROM V
						)
	"""
	curseur.execute(sql_query)


	connexion.commit()
except sqlite3.Error as er:
	print('SQLite error: %s' % (' '.join(er.args)))
	print("Exception class is: ", er.__class__)
	print('SQLite traceback: ')
	exc_type, exc_value, exc_tb = sys.exc_info()
	print(traceback.format_exception(exc_type, exc_value, exc_tb))

winner = curseur.fetchall()
print("Party with max votes: {}".format(winner))
#for i in winner:
	#print(winner)


#view for number of votes per candidat per party // number of votes = sum of "classement" --> smallest value = 1st position...

try:
	sql_query = """
		create view if not exists C(id_partie, nom_candidat, classement_sum) as SELECT id_partie, prenom, sum(vote_candidat.classement)
						 								FROM candidat, vote_candidat
						 								WHERE candidat.id = vote_candidat.id_candidat						 								
						 								GROUP BY id_partie, id_candidat
	"""
	curseur.executescript(sql_query)


	connexion.commit()
except sqlite3.Error as er:
	print('SQLite error: %s' % (' '.join(er.args)))
	print("Exception class is: ", er.__class__)
	print('SQLite traceback: ')
	exc_type, exc_value, exc_tb = sys.exc_info()
	print(traceback.format_exception(exc_type, exc_value, exc_tb))



#order of candidats per party
nbr_partis = 6
for i in range(nbr_partis):
	curseur.execute(""" select nom from partie where id=?
	""", (i,))
	req = curseur.fetchall()[0]
	for j in req:
		print("\nParti: {0}\n".format(j))
		curseur.execute("""select * from c where id_partie=? order by classement_sum
			""", (i,))
		q = curseur.fetchall()
		pos = 1
		for k in q:
			print(" Position numero {0}: {1}".format(pos,k[1]))
			pos += 1






connexion.close()