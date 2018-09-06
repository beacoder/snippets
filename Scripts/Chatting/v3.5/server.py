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

import os
import time
from socketserver import BaseRequestHandler, UDPServer


class EchoHandler(BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        print('Got message {msg} from {peer}.'.format(msg=data,
              peer=self.client_address))
        print('Sent message {msg} to {peer}.'.format(msg=data,
              peer=self.client_address))
        print('')
        sock.sendto(data, self.client_address)


def main():
    check_db()

    with UDPServer(('', 1223), EchoHandler) as serv:
        serv.serve_forever()


if __name__ == '__main__':
    main()
