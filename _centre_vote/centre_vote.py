import os, sys
from _connection import sender, fetch
main_dir, _ = os.path.split(os.path.abspath(os.getcwd()))
sys.path.append(main_dir)
import constants

# # # # # # # # # # # #
# Write here
#
# sender({
#		"src" : constants.CENTRE_VOTE,
#		"dest" : constants.<your_destination>, # Check constants.py
#		"body" : <your data>,
#		"to_string" : <your representation>
# })
#
# data = fetch()
# # # # # # # # # # # #


sender({
		"src" : constants.CENTRE_VOTE,
		"dest" : constants.CENTRE_VOTE, # Check constants.py
		"body" : 0,
		"to_string" : "Hello world"
})

data = fetch()