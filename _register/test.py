import os, sys
from _connection import fetch, sender
main_dir, _ = os.path.split(os.path.abspath(os.getcwd()))
sys.path.append(main_dir)
import constants

data = {
	"src": constants.REGISTER,
	"dest": constants.REGISTER,
	"body": 1000,
	"to_string": "Hello world"
}

sender(data)