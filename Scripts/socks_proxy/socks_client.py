#!/usr/bin/env python

import socket

class SocksClient(object):

    def __init__(self, addresss):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(address)

    def sync(self):
        """
        The client connects to the server, and sends a version
        identifier/method selection message:

        +----+----------+----------+
        |VER | NMETHODS | METHODS  |
        +----+----------+----------+
        | 1  |    1     | 1 to 255 |
        +----+----------+----------+
        """

        ver      = "\x05"
        nmethods = "\x01"
        mehods   = "\x00"

        self._socket.sendall()

        pass
