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

import logging
import socket
import struct
from chatting import eventloop, messagehandler


BUF_SIZE = 65536


class UDPClient(object):
    """Transmitting incomming/outgoing messages."""

    def __init__(self, server_addr, server_port, event_loop):
        self._server_addr = server_addr
        self._server_port = server_port
        self._msg_handler = None
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setblocking(False)
        event_loop.add(self._sock,
                       eventloop.POLL_IN | eventloop.POLL_ERR, self)

    def close(self):
        self._sock.close()

    def set_msg_handler(self, msg_handler):
        self._msg_handler = msg_handler

    def _on_send_data(self, data, dest):
        if data and dest:
            logging.debug("UDPClient: send data %s to %s" % (data, dest))
            self._sock.sendto(data, dest)

    def _on_recv_data(self):
        data, addr = self._sock.recvfrom(BUF_SIZE)
        if  data and addr:
            logging.debug("UDPClient: recved data %s" % data)
            (msg_type,), msg_body = struct.unpack(">B", data[:1]), data[1:]
            if self._msg_handler is not None:
                messagehandler.handle_message(msg_type, msg_body, addr, self._msg_handler)

    def send_message(self, msg):
        data = struct.pack(">B", msg.MSG_TYPE) + msg.to_bytes();
        self._on_send_data(data, (self._server_addr, self._server_port))

    def handle_event(self, sock, fd, event):
        if sock == self._sock:
            if event & eventloop.POLL_ERR:
                logging.error('UDP client_socket err')
            self._on_recv_data()
