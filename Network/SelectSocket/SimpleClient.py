# coding:utf-8

import socket
from Network import address

client_s = socket.socket()
client_s.connect(address)
# while True:
# data = raw_input("Send data:")
data = "ddddd"
client_s.send(data.encode())
data = client_s.recv(1024)
print data
client_s.close()
