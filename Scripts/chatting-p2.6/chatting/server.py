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

from __future__ import absolute_import, division, print_function, \
    with_statement

import sys
import os
import logging
import signal
import socket

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
from chatting import utils, eventloop, udpserver, messagereceiver, \
    messagehandler, messagedatabase


def main():
    host = socket.gethostbyname(socket.gethostname()) # the public network interface
    port = 5566
    udp_server = udpserver.UDPServer(host, port)
    msg_database = messagedatabase.MessageDatabase()
    msg_handler = messagehandler.MessageHandler(udp_server, msg_database)
    msg_recver = messagereceiver.MessageReceiver(msg_handler)
    udp_server.set_msg_recver(msg_recver)

    def int_handler(signum, _):
        sys.exit(1)
    signal.signal(signal.SIGINT, int_handler)

    try:
        event_loop = eventloop.EventLoop.default_loop()
        event_loop.add(udp_server.get_server_sock(),
                       eventloop.POLL_IN | eventloop.POLL_ERR, udp_server)
        event_loop.run()
    except Exception as e:
        utils.print_exception(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
