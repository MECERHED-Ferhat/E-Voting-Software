import subprocess as sb
import os

procs = []

root_path = os.path.abspath(os.getcwd())
router_path = os.path.join(root_path, "_routage")
user_app_path = os.path.join(root_path, "_user_app")

procs.append(sb.Popen(
	["python", os.path.join(router_path, "packets.py"), root_path],
	cwd=router_path
))
procs.append(sb.Popen(
	["python", os.path.join(user_app_path, "main.py"), root_path],
	cwd=user_app_path
))

input("Exit? (Enter)\n")

for proc in procs:
	try:
		proc.kill()
	except Exception as err:
		print(err)