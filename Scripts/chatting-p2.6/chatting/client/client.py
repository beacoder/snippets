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
import signal
import socket

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))
from chatting import utils, eventloop
from chatting.client import udpclient, chat


def main():
    utils.config_logging("/var/log/chatting_client.log");

    # server_addr = socket.gethostbyname(socket.gethostname())
    server_addr = '127.0.0.1'
    server_port = 5566
    event_loop = eventloop.EventLoop.default_loop()
    udp_client = udpclient.UDPClient(server_addr, server_port, event_loop)

    if hasattr(__builtins__, 'raw_input'):
        nick_name = raw_input("Please input your nick name!\n")
    elif hasattr(__builtins__, 'input'):
        nick_name = input("Please input your nick name!\n")
    chat_client = chat.ChatClient(nick_name, event_loop, udp_client)

    def int_handler(signum, _):
        sys.exit(1)
    signal.signal(signal.SIGINT, int_handler)

    try:
        print("Start your chat, e.g: 'nick: hello !'")
        chat_client.do_login()
        event_loop.run()
    except Exception as e:
        utils.print_exception(e)
        sys.exit(1)


if __name__ == '__main__':
    main()
