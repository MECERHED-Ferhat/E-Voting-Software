import threading, time, socket, sys, os, json
main_dir, _ = os.path.split(os.path.abspath(os.getcwd()))
sys.path.append(main_dir)
import constants


N_PORT = constants.REGISTER_PORT
N_PORT_REC = constants.REGISTER_PORT_REC


def listener():
	global BUFFER

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind(("127.0.0.1", N_PORT_REC))
		s.listen()
		while True:
			print("Listening... on ", N_PORT_REC)
			conn, addr = s.accept()
			print("register-listener connected")

			with conn:
				while True:
					try:
						data = conn.recv(8192)
					except Exception:
						continue
					if not data:
						break

					with open("__conn_register__.dat", "wb") as f:
						f.write(data)


def fetch():
	tmp = None
	with open("__conn_register__.dat", "wb") as f:
		pass
	while tmp is None:
		time.sleep(2)
		try:
			with open("__conn_register__.dat", "rb") as f:
				tmp = f.read() or None
		except Exception:
			continue
	with open("__conn_register__.dat", "wb") as f:
		pass

	return json.loads(tmp)["body"]


def sender(data):
	global BUFFER, N_PORT

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		while True:
			try:
				time.sleep(1)
				s.connect(("127.0.0.1", N_PORT))
			except Exception:
				pass
			else:
				break;
		print("register-sender connected")

		try:
			s.send(json.dumps(data, indent=2).encode("utf-8"))
		except Exception as e:
			print(e)
			

if __name__ == "__main__":

	threading.Thread(target=listener, daemon=True).start()

	while True:
		time.sleep(20)