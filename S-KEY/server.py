import socket
import string
import hashlib

HOST = '127.0.0.1'
PORT = 12345
BUFFERSIZE = 1024

def verify_passwrd(passwrd,msg):
    msg=hashlib.md5(msg.encode()).hexdigest()
    if msg == passwrd:
        return True
    return False

def main():
    d = dict()#словарь для хранения логина,пароля и числа итераций d[логин]={пароль,число итераций}
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    print("Socket binded to port ",PORT)
    s.listen(1)
    print("Socket listening on port ",PORT,"...")
    while True:
        client, addr = s.accept()
        print('Connection from ',addr, " is established")
        receive = client.recv(BUFFERSIZE)
        receive = receive.decode().rstrip()
        #получено сообщение об инициализации 
        if receive == "INITIATE":
            username = client.recv(BUFFERSIZE)
            username = username.decode().rstrip()
            n = client.recv(BUFFERSIZE)
            n = n.decode().rstrip()
            password = client.recv(BUFFERSIZE)
            password = password.decode().rstrip()
            #число итераций должно быть больше или равно 2
            if (int(n) >= 2):
                d.update({username:[password,int(n)]})#заносим в словарь новые данные 
                print("Initialized client record successful!")
            else:
                client.send("Small number n".ljust(BUFFERSIZE).encode())
                print("Failed initialization!")
                client.close()
       #получено сообщение об аутентификации 
        if receive == "AUTHENTICATE":
            username = client.recv(BUFFERSIZE)
            username = username.decode().rstrip()
           
            userdata = d.get(username)
            if  userdata == None: #если в словаре нет такого логина
                client.send("User not recognized".ljust(BUFFERSIZE).encode())
                client.close()
            else:
                client.send(str(userdata[1]).ljust(BUFFERSIZE).encode()) #отправляем клиенту n
                msg = client.recv(BUFFERSIZE)
                msg = msg.decode().rstrip() #y=hash(x)^n-1
                if verify_passwrd(userdata[0],msg): #сравниваем hash(y) и значение хэш-пароля из словаря
                    client.send("Success!".ljust(BUFFERSIZE).encode())
                    print("Authentication is successful")
                    x = userdata[1]-1 #уменьшаем n на 1
                    if x<2: #если n<2, то проводим реинициализацию 
                        client.send("REFRESH".ljust(BUFFERSIZE).encode())#отправляем клиенту сообщение о реинициализации
                        new_n = client.recv(BUFFERSIZE)# получаем новое число итераций
                        new_n = new_n.decode().rstrip()
                        newpass = client.recv(BUFFERSIZE)# новый хэш-пароль
                        newpass = newpass.decode().rstrip()
                        if int(new_n)>=2:
                            d.update({username:[newpass,int(new_n)]})# обновляем словарь
                            print("Refreshed client record!")
                        else:
                            client.send("Small number n".ljust(BUFFERSIZE).encode())
                            print("Failed to update!")
                            client.close()
                    else:
                    	client.send("NOREFRESH".ljust(BUFFERSIZE).encode())
                        d.update({username:[msg,x]})#если n>=2,то сохраняем в словаре новый хэш-пароль,уменьшенное число итераций
                else:
                    client.send("Fail!".ljust(BUFFERSIZE).encode())# hash(y) и значение хэш-пароля не совпали
                    print("Authentication is failed")
                    client.close()
            client.close()
                   

if __name__ == '__main__':
    main()     
