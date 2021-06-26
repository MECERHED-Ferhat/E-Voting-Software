import subprocess as sb
import os

procs = []

procs.append(sb.Popen(
	["python", "packets.py"]
))
procs.append(sb.Popen(
	["python", "main.py"]
))

input("Exit? (Enter)\n")

for proc in procs:
	try:
		proc.kill()
	except Exception as err:
		print(err)