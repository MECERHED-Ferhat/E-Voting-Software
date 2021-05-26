import sqlite3, sys, traceback

connexion = sqlite3.connect("../database.db")
curseur = connexion.cursor()

try:
	sql_query = """
	CREATE TABLE IF NOT EXISTS Electeur (
		id 						VARCHAR(18),
		nom 					VARCHAR(255),
		prenom 				VARCHAR(255),
		H_PIN 				VARCHAR(64),
		Eligible 			BOOLEAN,

		CONSTRAINT PK_Electeur PRIMARY KEY (id)
	);

	CREATE TABLE IF NOT EXISTS Partie (
		id 						INT,
		nom 					VARCHAR(255),
		image 				VARCHAR(255),

		CONSTRAINT PK_Partie PRIMARY KEY (id)
	);

	CREATE TABLE IF NOT EXISTS Candidat (
		id 						INT,
		nom 					VARCHAR(255),
		prenom 				VARCHAR(255),
		image 				VARCHAR(255),
		classement 		INT,
		id_partie 		INT,

		CONSTRAINT PK_Candidat PRIMARY KEY (id, id_partie),
		CONSTRAINT FK_Candidat_in_Partie
			FOREIGN KEY (id_partie)
			REFERENCES Partie(id)
			ON DELETE CASCADE
	);

	CREATE TABLE IF NOT EXISTS Vote (
		id 						INT,
		id_partie 		INT,

		CONSTRAINT PK_Vote PRIMARY KEY (id),
		CONSTRAINT FK_Vote_for_Partie
			FOREIGN KEY (id_partie)
			REFERENCES Partie(id)
			ON DELETE CASCADE
	);

	CREATE TABLE IF NOT EXISTS Vote_Candidat (
		id_vote 			INT,
		id_candidat 	INT,
		classement 		INT,

		CONSTRAINT PK_VoteCandidat PRIMARY KEY (id_candidat, id_vote),
		CONSTRAINT FK_VoteCandidat_in_Vote
			FOREIGN KEY (id_vote)
			REFERENCES Vote(id)
			ON DELETE CASCADE,
		CONSTRAINT FK_VoteCandidat_for_Candidat
			FOREIGN KEY (id_candidat)
			REFERENCES Candidat(id)
			ON DELETE CASCADE
	);
	"""
	curseur.executescript(sql_query)



	connexion.commit()
except sqlite3.Error as er:
	print('SQLite error: %s' % (' '.join(er.args)))
	print("Exception class is: ", er.__class__)
	print('SQLite traceback: ')
	exc_type, exc_value, exc_tb = sys.exc_info()
	print(traceback.format_exception(exc_type, exc_value, exc_tb))


connexion.close()