import hashlib
import hmac
import os,socket,time

dir_name = 'C:\pythonProjectpp'
list_of_files = filter( lambda x: os.path.isfile(os.path.join(dir_name, x)),
                        os.listdir(dir_name) )
files_with_size = [ (file_name, os.stat(os.path.join(dir_name, file_name)).st_size)
                    for file_name in list_of_files  ]
filesize=int(input("Enter file size"))
start = time.time()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((socket.gethostname(), 22222))
sock.listen(5)
print("HOST: ", sock.getsockname())
client, addr = sock.accept()
i=0
for file_name, size in files_with_size:
    if(size==filesize):

        file = file_name
        filesize = size

        client.send(file.encode())
        client.send(str(filesize).encode())

        def setup(file,i):
            file_obj = open(file, 'rb')
            file_data = file_obj.read()
            mac = hmac.new(b'newsecret', file_data, hashlib.sha256).hexdigest()
            with open(('mac'+str(i)+'.txt'), 'wb') as fout:
                fout.write(mac.encode())
                client.send(fout.encode())
                client.send(str(os.path.getsize(fout)).encode())
                c = 0
                while c <= (os.path.getsize(fout)):
                    data = fout.read(1024)
                    if not (data):
                        break
                    client.sendall(data)
                    c += len(data)
            print("MAC generated")
            file_obj.close();


        setup(file,i)
        i+=1
        with open(file, "rb") as file:
            c = 0
            while c <= filesize:
                data = file.read(1024)
                if not (data):
                    break
                client.sendall(data)
                c += len(data)

        # with open(filename, "wb") as file:
        #         c = 0
        #         start = time.time()
        #         while c <= int(filesize):
        #             data = sock.recv(1024)
        #             if not (data):
        #                 break
        #             file.write(data)
        #             c += len(data)
        #         end = time.time()

end = time.time()
print("Transfer Complete. Total time:", end - start)

sock.close()