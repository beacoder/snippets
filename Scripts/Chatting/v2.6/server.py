#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2018-2018 humingchen
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import socket


BUF_SIZE = 65536


class UDPServer(object):

    def __init__(self,host,port):
        self._host = host
        self._port = port
        self._clients = set()

    def __enter__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self._host,self._port))
        self._sock = sock
        return self

    def __exit__(self,*exc_info):
        if exc_info[0]:
            import traceback
            traceback.print_exception(*exc_info)
        self._sock.close()

    def handle_connections(self):
        """recv msg from clients."""

        data, addr = self._sock.recvfrom(BUF_SIZE)
        self._clients.add(addr)

        print('Got message {msg} from {peer}.'.format(msg=data, peer=addr))
        print('')

        for addr in self._clients:
            self._sock.sendto(data, addr)


def main():
    host = socket.gethostbyname(socket.gethostname()) # the public network interface
    port = 5566
    with UDPServer(host,port) as server:
        while True:
            server.handle_connections()


if __name__ == '__main__':
    main()
