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


def main():
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
        words = [b"Hello\n", b"World\n", b"!\n"]
        while True:
            data = random.choice(words)
            addr = ('localhost', 1223)
            print('Sent message {msg} to {peer}.'.format(msg=data, peer=addr))
            sock.sendto(data, addr)
            time.sleep(1)
            data, addr = sock.recvfrom(BUF_SIZE)
            print('Got message {msg} from {peer}.'.format(msg=data, peer=addr))
            print('')
            time.sleep(1)


if __name__ == '__main__':
    main()
