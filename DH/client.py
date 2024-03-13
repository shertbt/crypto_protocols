#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from math import ceil 
from secrets import randbits
import random
from hashlib import sha1
import socket

HOST = '127.0.0.1'
PORT = 5050 

def pow_2(num):
	pow_2 = 0
	while True:
		if num & 1 == 0:
			num >>= 1
			pow_2 += 1
		else:
			return pow_2
#тест Миллера-Рабина
def is_prime(q):
	i = 1
	n = 50
	w = q
	a = pow_2(w-1)
	m = (w-1) // pow(2,a)
	while True:
		b = random.randrange(1,w)
		j = 0
		z = pow(b, m, w)
		while True:
        
			if (j == 0 and z == 1) or z == w - 1:
				if i < n:
					i = i + 1
					break
				else:
					return True
			if j > 0 and z == 1:
				return False
			j += 1
			if j < a:
				z = pow(z, 2, w)
				continue
			return False
 

                    
def generate_pq(m, L):
	m_1 = ceil(m / 160)
	L_1 = ceil(L / 160)
	N = ceil(L / 1024)
	prime = False

	while not prime:	
		seedlen = m_1 + random.randint(0,128)
		seed = randbits(seedlen)
		U = 0
		for i in range(m_1):
			seed1 = seed + i
			seed1_hash = sha1(seed1.to_bytes(ceil(seed1.bit_length() / 8), "big")).digest()
			seed2 = (seed+m+i) % pow(2, seedlen)
			seed2_hash = sha1(seed2.to_bytes(ceil(seed2.bit_length() / 8), "big")).digest()
			xor = int.from_bytes(seed1_hash, "big") ^ int.from_bytes(seed2_hash, "big")
			U = U + xor * pow(2, 160 * i)
			
		q = U % pow(2,m)
		q = q | (1 << 0)
		q = q | (1 << m-1)
		prime = is_prime(q)
        
	counter = 0
	while True:
		R = seed + 2 * m_1 + L_1 * counter
		V = 0
		for i in range(L_1 - 1):
			R_hash = sha1((R+i).to_bytes(ceil((R+i).bit_length() / 8), "big") ).digest()
			V = V + int.from_bytes(R_hash, "big") * pow(2, 160 * i)
		W = V % pow(2, L)
		X = W | pow(2, L - 1)
		p = X - (X % (2 * q)) + 1

		if p > pow(2, L- 1) and is_prime(p):
			return (p, q, seed, counter) 
		counter += 1

		if counter < (4096 * N):
			continue
		return False
        
def generate_g(p,q):
	j = (p-1) // q
	while(True):
		h = random.randint(1, p-1)
		g = pow(h,j, p)
		if (g != 1):
			return g
		return g 
			
def generate_params():
	while True:
		p, q, seed, counter = generate_pq(128,1024)
		g = generate_g(p,q)
		x = random.randrange(2, q-2)
		y = pow(g,x,p)
		if is_correct(y,p,q):
			break
	return (x,y,g,p)

def is_correct(y,p,q):
	if y < 2 or y > p-1:
		return False
	if (pow(y,q,p) != 1):
		return False
	return True	
	
if __name__ == "__main__":
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((HOST, PORT))
	secret, public, g, p = generate_params()
	message = str(p) + "||" + str(g) +"||" + str(public)
	sock.sendall(message.encode())
	print(f"p={p}")
	print(f"g={g}")
	print(f"public key={public}")
	print(f"private key={secret}")
	resp = sock.recv(2048).decode()  
	public_bob = int(resp)
	key = pow(public_bob, secret, p)
	print(f"key={key}")
