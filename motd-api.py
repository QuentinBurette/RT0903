import socket
import json
import sys


HOST=''

if len( sys.argv ) == 3:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, int(sys.argv[2])))
	s.listen(5)
	x = json.dumps(sys.argv[1])

	while True:
		conn, addr = s.accept()
		print("Connecté par: ",addr)
		print("Message: ", x )
		print(x)
		conn.send(("Success").encode())
		conn.close()
		exit()
else :
	print("Erreur arguments")

