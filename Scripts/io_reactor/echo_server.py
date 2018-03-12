#!/usr/bin/env python

"""use this echo server to test socket funciton."""


import socket
from reactor.reactor import Reactor
from reactor.event_handler import EventHandler
from reactor.demux.demux import POLL_IN


class SocketReader(EventHandler):
    """
    Recv data from and send data to client.
    """

    # maybe we should use a separate thread to do this.
    def handle_input(self, sock, fd):
        data = sock.recv(4096)
        if data:
            print "Recved data from connection {0}".format(sock.getpeername())
            print data.__repr__()
            print
        pass

    pass


class SocketAcceptor(EventHandler):
    """Accept socket connection from client."""

    def handle_input(self, sock, fd):
        if fd == s.fileno():
            (c, addr) = sock.accept()
            c.setblocking(False)
            r.register_handler(c, POLL_IN, SocketReader())
            print "Accepted one connection from address {0}".format(addr)
            print
        pass

    pass


def test():
    global r, s
    r = Reactor()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((socket.gethostname(), 10010))
    s.listen(10)

    r.register_handler(s, POLL_IN, SocketAcceptor())
    r.handle_events()

    pass


if __name__=='__main__':
    test()
