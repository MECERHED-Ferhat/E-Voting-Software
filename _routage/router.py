import threading, time, socket, sys, os, json, pickle
main_dir, _ = os.path.split(os.path.abspath(os.getcwd()))
sys.path.append(main_dir)
import constants

BUFFER = {
	constants.USER_APP: None,
	constants.REGISTER: None,
	constants.CENTRE_VOTE: None,
	constants.XXXX: None
}

def listener(nport):
	global BUFFER

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.bind(("127.0.0.1", nport))
		s.listen()
		while True:
			print("Listening... on ", nport)
			conn, addr = s.accept()
			print("router-listener connected on ", nport)

			with conn:
				while True:
					try:
						data = conn.recv(4096)
					except Exception:
						break
					if not data:
						break

					tmp = json.loads(data.decode("utf-8"))

					with open("__conn_tmp__.dat", "ab") as f:
						pickle.Pickler(f).dump(tmp)

					if ("dest" in tmp):
						BUFFER[tmp["dest"]] = tmp

def sender(nport, dest):
	global BUFFER

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		while True:
			try:
				time.sleep(1)
				s.connect(("127.0.0.1", nport))
			except Exception:
				pass
			else:
				break;
		print("Connected to ", dest)

		while True:
			while BUFFER[dest] is None:
				time.sleep(1)

			s.send(json.dumps(BUFFER[dest], indent=2).encode("utf-8"))
			BUFFER[dest] = None



if __name__ == "__main__":

	for i in (constants.USER_APP_PORT, constants.REGISTER_PORT, constants.XXXX_PORT, constants.CENTRE_VOTE_PORT):
		threading.Thread(target=listener, args=(i,), daemon=True).start()

	threading.Thread(target=sender, args=(constants.USER_APP_PORT_REC, constants.USER_APP), daemon=True).start()
	threading.Thread(target=sender, args=(constants.REGISTER_PORT_REC, constants.REGISTER), daemon=True).start()
	threading.Thread(target=sender, args=(constants.CENTRE_VOTE_PORT_REC, constants.CENTRE_VOTE), daemon=True).start()
	threading.Thread(target=sender, args=(constants.XXXX_PORT_REC, constants.XXXX), daemon=True).start()

	while True:
		time.sleep(20)