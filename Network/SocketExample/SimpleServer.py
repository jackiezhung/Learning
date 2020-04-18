# coding:utf-8

import socket
from Network import address


server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_s.bind(address)
server_s.listen(5)
print("Start server on: {}".format(address))
while True:
    client_s, client_addr = server_s.accept()
    print("Connect from {}".format(client_addr))
    while True:
        receive = client_s.recv(1024)
        if receive != b"exit":
            print(receive.decode())
        else:
            client_s.close()
            print("Disconnect from {}".format(client_addr))
            break
