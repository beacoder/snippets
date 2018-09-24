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
from chatting import eventloop, message, messagehandler


class ChatClient(messagehandler.IMessageHandler):
    """Gui for chatting."""

    def __init__(self, nick_name, event_loop, msg_transceiver):
        self._nick_name = nick_name
        event_loop.add(sys.stdin,
                       eventloop.POLL_IN | eventloop.POLL_ERR, self)
        self._transceiver = msg_transceiver
        self._transceiver.set_msg_handler(self)

    def do_login(self):
        logging.info("sending login req.")
        self._transceiver.send_message(message.LoginReq(self._nick_name))

    def handle_login_rsp(self, login_rsp, src_addr):
        if login_rsp.result:
            logging.info("logging success.")

    def handle_chat_msg(self, chat_msg, src_addr):
        msg_from = chat_msg.msg_to
        msg_content = chat_msg.msg_content
        if msg_from and msg_content:
            print("%s: %s" % (msg_from, msg_content))

    def handle_broadcast_msg(self, broadcast_msg, src_addr):
        pass

    def _handle_input(self):
        raw_msg = sys.stdin.readline()
        msg_to = raw_msg.split(":")[0].strip()
        msg = ":".join(raw_msg.split(":")[1:]).strip()
        if msg_to and msg:
            if len(msg) > 1024:
                raise Exception("Max message length reached: 1024!")
            self._transceiver.send_message(message.ChatMessage(msg_to, msg))

    def handle_event(self, sock, fd, event):
        if fd == sys.stdin.fileno():  # handle input from sys.stdin
            if event & eventloop.POLL_ERR:
                logging.error('ChatClient err')
            self._handle_input()


def test_message_available():
    assert hasattr(message, 'LoginReq')
    assert hasattr(message, 'LoginRsp')
    assert hasattr(message, 'ChatMessage')


if __name__ == '__main__':
    test_message_available()
