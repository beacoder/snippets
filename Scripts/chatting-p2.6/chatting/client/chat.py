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
import logging
import socket
import struct
from chatting import message


BUF_SIZE = 65536


class ChatClient(object):
    """Gui for chatting."""

    def __init__(self, event_loop, msg_sender):
        event_loop.add(sys.stdin,
                       eventloop.POLL_IN | eventloop.POLL_ERR, self)
        self._msg_sender = msg_sender

    def run(self):
        while not self._stopping:
            try:
                raw_msg = raw_input("Please input your chat message, e.g: nick: hello !")
                msg_to = raw_msg.split(":")[0].strip()
                msg = ":".join(raw_msg.split(":")[1:]).strip()
                if msg_to and msg:
                    if len(msg) > 1024:
                        raise Exception("Max message length reached: 1024!")
                    chat_msg = ChatMessage(msg_to, msg_content)
                    self._out_msg_queue.put(chat_msg)


            except Exception as e:
                print("run: %s", e)
                continue


    def send_message(self, msg, to_addr):
        data = struct.pack(">H", msg.MSG_TYPE) + msg.to_bytes();
        print('Sent message {msg} to {peer}.'.format(msg=data, peer=to_addr))
        self._out_msg_queue.put(data)

    def _handle_input(self):
        # raw_msg = raw_input("Please input your chat message, e.g: nick: hello !")
        raw_msg = sys.stdin.readline()
        msg_to = raw_msg.split(":")[0].strip()
        msg = ":".join(raw_msg.split(":")[1:]).strip()
        if msg_to and msg:
            if len(msg) > 1024:
                raise Exception("Max message length reached: 1024!")
            self._msg_sender.send_message(ChatMessage(msg_to, msg_content))

    def handle_event(self, sock, fd, event):
        if fd == sys.stdin:
            if event & eventloop.POLL_ERR:
                logging.error('ChatClient err')
            try:
                self._handle_input()
            except Exception as e:
                print ("handle_input: %s", e)
        pass
