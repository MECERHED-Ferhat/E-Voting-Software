import socket, json
from time import sleep

HOST = "127.0.0.1"
PORT = 4444

def get_data():
	data = []
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		while True:
			try:
				sleep(3)
				s.connect((HOST, PORT))
			except ConnectionRefusedError as e:
				pass
			else:
				break;


		##############################
		res = {
			"request" : "GET_DATA",
		}
		
		s.send(json.dumps(res, indent=2).encode("utf-8"))
		
		data = json.loads(s.recv(4096).decode("utf-8"))
		##############################

	return data