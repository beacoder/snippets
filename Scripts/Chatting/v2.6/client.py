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

import random
import socket
import time

BUF_SIZE = 65536

class UDPClient(object):

    def __init__(self):
        self._data = [b"Hello\n", b"World\n", b"!\n"]
        pass

    def __enter__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock = sock
        return self

    def __exit__(self,*exc_info):
        if exc_info[0]:
            import traceback
            traceback.print_exception(*exc_info)
        self._sock.close()

    def recv_msg(self):
        """recv msg from server."""

        data, addr = self._sock.recvfrom(BUF_SIZE)
        print('Got message {msg} from {peer}.'.format(msg=data, peer=addr))
        print('')
        time.sleep(1)

    def send_msg(self, dest, port):
        """send msg to server."""

        data = random.choice(self._data)
        addr = (dest, port)
        print('Sent message {msg} to {peer}.'.format(msg=data, peer=addr))
        self._sock.sendto(data, addr)
        time.sleep(1)

def main():
    dest = socket.gethostbyname(socket.gethostname())
    port = 5566
    with UDPClient() as client:
        while True:
            client.send_msg(dest, port)
            client.recv_msg()

if __name__ == '__main__':
    main()
