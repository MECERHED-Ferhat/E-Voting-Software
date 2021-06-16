USER_APP = "Application Utilisateur"
USER_APP_PORT = 4444
USER_APP_PORT_REC = 4448
REGISTER = "Serveur Registre"
REGISTER_PORT = 4445
REGISTER_PORT_REC = 4449
XXXX = "XXXX"
XXXX_PORT = 4446
XXXX_PORT_REC = 4450
CENTRE_VOTE = "Centre Vote"
CENTRE_VOTE_PORT = 4447
CENTRE_VOTE_PORT_REC = 4451
"""
res = {
	"src" : constants.USER_APP,
	"dest" : constants.REGISTER,
	"body" : {	
		"request" : "AUTH",
		"elec" :  electeur
		},
	"to_string" : "Authentification"
}
"""