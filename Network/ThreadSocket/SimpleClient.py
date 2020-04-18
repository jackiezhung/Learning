# coding:utf-8

import socket
from Network import address

client_s = socket.socket()
client_s.connect(address)
while True:
    data = input("Send data:")
    client_s.send(data.encode())
