import sqlite3, sys, traceback

connexion = sqlite3.connect("../../database.db")
curseur = connexion.cursor()

try:
	sql_query = """
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