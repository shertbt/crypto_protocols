#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket 
import random
import string
import hashlib
import struct
import time

IP = "127.0.0.1"
PORT = 9090
CLIENT_SECRET = "secret"
size = struct.calcsize('>ss32s')

def make_challenge(user_id, num):	
	package=struct.pack('>ssi',"1",str(user_id),num)
	return package
	
def make_success(user_id):
	package=struct.pack('>ssi',"3",str(user_id),0)
	return package
	
def make_fail(user_id):
	package=struct.pack('>ssi',"4",str(user_id),0)
	return package

def check_answer(asw, num):
	msg=struct.unpack('>ss32s', asw)
	code = msg[0]
	client_id = msg[1]
	client_num = msg[-1]
	print(msg)
	if (code != "2"):
		print("Error code of response package")
		return False
	
	hsh = client_id + CLIENT_SECRET + str(num)
	hsh = hashlib.md5(hsh.encode()).hexdigest()
	print(hsh)
	if (client_num == hsh):
		return True
	return False


def main():
	sock = socket.socket()
	sock.bind((IP, PORT))
	sock.listen(3)
	print("Socket listening on port ",PORT,"...")

	while True:
	  try:
		conn, addr = sock.accept()
		print('Connection from ',addr, " is established")
		# идентификатор - номер сессии
		user_id = 0
		
		while True:
			
		#make package 1|u_id|rand_int
			num = random.randint(1, 1024)
			package = make_challenge(user_id, num)
			conn.sendall(package)
		# 2|u_id|value - можно после id длину value, но зачем
			user_answer = conn.recv(size)
			if (check_answer(user_answer, num)):
			#make package 3|u_id
				package = make_success(user_id)
				conn.sendall(package)
				print("Success!")
				time.sleep(3)
				user_id+=1
				if(user_id>9):
					conn.close()
					break
				continue
			else:
			#make package 4|u_id
				package = make_fail(user_id)
				conn.sendall(package)
				print("Fail!")
				conn.close()
	  except:
	  	print("Disconnect")
	  	break


if __name__ == '__main__':
	main()  
