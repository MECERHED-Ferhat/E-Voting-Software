import subprocess as sb
import os

procs = []

root_path = os.path.abspath(os.getcwd())
router_path = os.path.join(root_path, "_routage")
register_path = os.path.join(root_path, "_register")
user_app_path = os.path.join(root_path, "_user_app")
centre_vote_path = os.path.join(root_path, "_centre_vote")
xxxx_path = os.path.join(root_path, "_xxxx")

procs.append(sb.Popen(
	["python", os.path.join(router_path, "router.py"), root_path],
	cwd=router_path
))
procs.append(sb.Popen(
	["python", os.path.join(register_path, "_connection.py"), root_path],
	cwd=register_path
))
procs.append(sb.Popen(
	["python", os.path.join(register_path, "register.py"), root_path],
	cwd=register_path
))
procs.append(sb.Popen(
	["python", os.path.join(user_app_path, "_connection.py"), root_path],
	cwd=user_app_path
))
procs.append(sb.Popen(
	["python", os.path.join(centre_vote_path, "_connection.py"), root_path],
	cwd=centre_vote_path
))
procs.append(sb.Popen(
	["python", os.path.join(xxxx_path, "_connection.py"), root_path],
	cwd=xxxx_path
))

input("Exit? (Enter)\n")

for proc in procs:
	try:
		proc.kill()
	except Exception as err:
		print(err)