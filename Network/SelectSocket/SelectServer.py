# coding:utf-8

import socket
import threading
try:
    import queue
    from queue import Queue
except ImportError:
    import Queue as queue
    from Queue import Queue
from Network import address
from select import select

msg_queue = {}
inputs = []
outputs = []


def main_thread():
    """"""
    server_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_s.bind(address)
    server_s.listen(10)
    # 设置为非阻塞
    server_s.setblocking(False)
    print("Start server on: {}".format(address))
    inputs.append(server_s)

    while True:
        readable, writeable, errors = select(inputs, outputs, inputs)
        for sc in readable:
            if sc == server_s:
                client_s, client_addr = server_s.accept()
                client_s.setblocking(False)
                msg_queue[client_s] = Queue()
                inputs.append(client_s)
            else:
                data = sc.recv(1024)
                if data:
                    if sc not in outputs:
                        outputs.append(sc)
                    _msg = "sc: %s, receive data: %s" % (sc, data)
                    print(_msg)
                    msg_queue[sc].put(_msg)
                else:
                    if sc in outputs:
                        outputs.remove(sc)
                    inputs.remove(sc)
                    sc.close()
        for sc in writeable:
            try:
                msg = msg_queue[sc].get_nowait()
            except queue.Empty:
                if sc in outputs:
                    outputs.remove(sc)
            else:
                print("send data to: %s, data:%s" % (sc, msg))
                sc.send(msg.encode())
        for sc in errors:
            inputs.remove(sc)
            if sc in outputs:
                outputs.remove(sc)
            sc.close()
            del msg_queue[sc]


if __name__ == '__main__':
    main_thread()
