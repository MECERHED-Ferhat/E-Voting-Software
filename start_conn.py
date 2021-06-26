import subprocess as sb
import os

procs = []

procs.append(sb.Popen(
	["python", "register.py"]
))
procs.append(sb.Popen(
	["python", "router.py"]
))
procs.append(sb.Popen(
	["python", "_connection_centre_vote.py"]
))
procs.append(sb.Popen(
	["python", "_connection_register.py"]
))
procs.append(sb.Popen(
	["python", "_connection_server.py"]
))
procs.append(sb.Popen(
	["python", "_connection_user_app.py"]
))

input("Exit? (Enter)\n")

for proc in procs:
	try:
		proc.kill()
	except Exception as err:
		print(err)