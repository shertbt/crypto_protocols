#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
from hashlib import sha1
from secrets import SystemRandom
HOST = '127.0.0.1'
PORT = 5050 

if __name__ == "__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((HOST, PORT))
	sock.listen(1)
	print('Боб:')
	while True:
		conn, addr = sock.accept()
		print(f"Новое подключение: {addr}")
		dh_parameters= conn.recv(2048).decode().split("||")
		p=int(dh_parameters[0])
		g=int(dh_parameters[1])
		A=int(dh_parameters[2])
		rand = SystemRandom()
		private = rand.randrange(2, p-2)
		public = pow(g, private, p)
		print(f"p={p}")
		print(f"g={g}")
		print(f"public key={public}")
		print(f"private key={private}")
		conn.sendall(str(public).encode())
		key = pow(A, private, p)
		print(f"key={key}")
