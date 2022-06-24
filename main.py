import hashlib
import hmac

import os, socket,time

host=input("Enter Host Name:")
sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    sock.connect((host,22222))
    print("Connected")
except:
    print("Unable to connect")
    exit(0)
filename=sock.recv(100).decode()
filesize=sock.recv(100).decode()


def verify(filename):
    file_obj = open(filename, 'rb')
    file_data = file_obj.read()
    mac1 =str( hmac.new(b'newsecret', file_data, hashlib.sha256).hexdigest())
    # print(mac1)
    mac = sock.recv(100).decode()
    macsize = sock.recv(100).decode()
    file_obj1 = open(mac, 'rb')
    file_data1 = file_obj1.read()
    # print(file_data1.decode())
    with open(mac, "wb") as file:
        c = 0
        while c <= int(macsize):
            data = sock.recv(1024)
            if not (data):
                break
            file.write(data)
            c += len(data)
    if (mac1 == str(file_data1.decode())):
         print("Verified")
    else:
        print("Verification failed")

 verify(filename)

with open(filename,"wb")as file:
    c=0
    start=time.time()
    while c<=int(filesize):
        data=sock.recv(1024)
        if not (data):
            break
        file.write(data)
        c+=len(data)
    end=time.time()
print("Transfer Complete. Total time:" ,end-start)
sock.close()