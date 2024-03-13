#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import hashlib
import struct

IP = "127.0.0.1"
PORT = 9090
password = "paswd"
size = struct.calcsize('>ssi')
def md5(msg):
    hash_msg = hashlib.md5(msg.encode()).hexdigest()
    return hash_msg

def solve_challenge(msg,password):
    ID=msg[1]
    num=msg[-1]
    hash_msg = md5(ID+password+str(num))
    resp=struct.pack('>ss32s',"2",ID,hash_msg)
    return resp
    
def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((IP, PORT))
    
    try:
    	while True:	
        	pack=server.recv(size)
		msg=struct.unpack('>ssi', pack)
        	if(msg[0]=="1"):
            		print("Challenge!")
            		response=solve_challenge(msg,password)
            		server.sendall(response)
        	if(msg[0]=="3"):
            		print("Success!")
   
        	if(msg[0]=="4"):
            		print("Fail!")
            		server.close()
    except:
    	server.close()
    	print("Disconnect")
    
if __name__ == '__main__':
    main()
