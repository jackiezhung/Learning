#coding:utf-8
#!/usr/bin/env python
import select
import socket
import queue
address = ('0.0.0.0', 8080)
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(address)
serversocket.listen(1)
serversocket.setblocking(False)
msg_queue = {}
print("Start up server %s on port %s" % address)

READ_ONLY = (select.EPOLLIN | select.EPOLLPRI | select.EPOLLHUP | select.EPOLLERR)
READ_WRITE = (READ_ONLY | select.EPOLLOUT)

epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)

fd_socket = {serversocket.fileno(): serversocket}
while True:
    events = epoll.poll(1)
    for fd, event in events:
        sc = fd_socket[fd]
        if event & (select.EPOLLIN | select.EPOLLPRI):
            if sc == serversocket:
                client, address = serversocket.accept()
                print('client connected:', address)
                client.setblocking(False)
                epoll.register(client.fileno(), READ_ONLY)
                fd_socket[client.fileno()] = client
                msg_queue[client] = queue.Queue()
            else:
                data = sc.recv(1024)
                if data:
                    print("receive data:%s from: %s" % (data, sc.getpeername()))
                    msg_queue[sc].put(data)
                    epoll.modify(sc, READ_WRITE)
                else:
                    print("closing", sc.getpeername())
                    epoll.unregister(sc)
                    sc.close()
                    del msg_queue[sc]
        elif event & select.EPOLLOUT:

            try:
                msg = msg_queue[sc].get_nowait()
            except queue.Empty:
                epoll.modify(sc, READ_ONLY)
            else:
                print("-------send data---------", msg)
                sc.send(msg)
        elif event & select.EPOLLHUP:
            print("end hup------")
            epoll.unregister(sc)
            sc.close()
            del msg_queue[sc]
        elif event & select.EPOLLERR:
            print("exception on", sc.getpeername())
            epoll.unregister(sc)
            sc.close()
            del msg_queue[sc]