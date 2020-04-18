# coding:utf-8

import socket
import threading
from Network import address


server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_s.bind(address)
server_s.listen(5)
print("Start server on: {}".format(address))


def client_thread(cs, ca):
    while True:
        receive = cs.recv(1024)
        if receive != b"exit":
            print("ca:{}, data:{}".format(ca, receive.decode()))
        else:
            cs.close()
            print("Disconnect from {}".format(ca))
            break


def main_thread():
    while True:
        client_s, client_addr = server_s.accept()
        print("Connect from {}".format(client_addr))
        th = threading.Thread(target=client_thread, args=(client_s, client_addr))
        th.setDaemon(True)
        th.start()


if __name__ == '__main__':
    main_thread()