import socket
import select
import queue


address = ("192.168.188.133", 10000)

# create a Tcp/ip socket and bind and listen
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Startup on %s, port %s" % address)

server.bind(address)
server.listen(5)
msg_queue = {}

timeout = 1000

READ_ONLY = (select.POLLIN | select.POLLPRI | select.POLLHUP | select.POLLERR)
READ_WRITE = (READ_ONLY | select.POLLOUT)

polls = select.poll()
polls.register(server, READ_ONLY)
fd_socket = {server.fileno(): server}
while True:
    # print("Wait next event.")
    events = polls.poll(timeout)
    # print("*" * 20)
    # print(len(events))
    # print(events)
    # print("*" * 20)
    for fd, flag in events:
        s = fd_socket[fd]
        if flag & (select.POLLIN | select.POLLPRI):
            if s is server:
                client, client_address = s.accept()
                print("Connect from " , client_address)
                fd_socket[client.fileno()] = client
                client.setblocking(False)
                polls.register(client, READ_ONLY)
                msg_queue[client] = queue.Queue()
            else:
                data = s.recv(1024)
                if data:
                    print("receive data:%s from: %s" % (data, s.getpeername()))
                    msg_queue[s].put(data)
                    polls.modify(s, READ_WRITE)
                else:
                    print("closing", s.getpeername())
                    polls.unregister(s)
                    s.close()
                    del msg_queue[s]
        elif flag & select.POLLHUP:
            print("Closing", s.getpeername(), "HUP")
            polls.unregister(s)
            s.close()
        elif flag & select.POLLOUT:
            try:
                next_msg = msg_queue[s].get_nowait()
            except queue.Empty:
                print(s.getpeername(), "queue empty")
                polls.modify(s, READ_ONLY)
            else:
                print("sending %s to %s" % (next_msg, s.getpeername()))
                s.send(next_msg)
        elif flag & select.POLLERR:
            print("exception on", s.getpeername())
            polls.unregister(s)
            s.close()
            del msg_queue[s]

