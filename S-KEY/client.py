#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import hashlib

def myhash(passwd):
	return hashlib.md5(passwd.encode()).hexdigest()

sock = socket.socket()
sock.connect(('localhost', 8080))


act = input("What do you want:\nINITIATE - New client/Reinitialization\nAUTHENTICATE - Start authentication\n")

sock.send(act.ljust(1024).encode())
#инициализация 
if act == "INITIATE":
	username = input("Enter username: ")
	password = input("Enter password: ")
	num = input("Enter number of iteration: ")
	hashedpassw = password
	for i in range(int(num)):
		hashedpassw = myhash(hashedpassw)		
	#отправить имя пароль-хэш и число итераций
	sock.send(username.ljust(1024).encode())
	sock.send(num.ljust(1024).encode())
	sock.send(hashedpassw.ljust(1024).encode())
	sock.close()
	
#аутентификация
if act == "AUTHENTICATE":
	username = input("Enter username: ")
	sock.send(username.encode())
	#если имя валидное - ответ n, иначе error
	resp = sock.recv(1024).decode().rstrip()
	
	if (resp != "User not recognized"):
		password = input("Enter password: ")
		hashedpassw = password
		for i in range(int(resp)-1):
			hashedpassw = myhash(hashedpassw)
		sock.send(hashedpassw.encode())
	else:
		print(resp)
		sock.close()
		exit(0)
	resp = sock.recv(1024).decode().rstrip()
	print(resp)
	resp = sock.recv(1024).decode().rstrip()
	if (resp == "REFRESH"):
		num = input("Your password has expired! Please, refresh password!\nEnter new number of iteration: ")
		password = input("Enter new password: ")
		hashedpassw = password
		for i in range(int(num)):
			hashedpassw = myhash(hashedpassw)
		sock.send(num.ljust(1024).encode())
		sock.send(hashedpassw.ljust(1024).encode())
	sock.close()
		
				


