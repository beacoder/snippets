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
from chatting import eventloop, message, messagehandler


BUF_SIZE = 65536


class UDPServer(object):
    """Transmitting incomming/outgoing messages."""

    def __init__(self, host, port, event_loop):
        self._listen_addr = host
        self._listen_port = port
        self._msg_handler = None
        addrs = socket.getaddrinfo(self._listen_addr, self._listen_port, 0,
                                   socket.SOCK_DGRAM, socket.SOL_UDP)
        if len(addrs) == 0:
            raise Exception("can't get addrinfo for %s:%d" %
                            (self._listen_addr, self._listen_port))
        af, socktype, proto, canonname, sa = addrs[0]
        server_socket = socket.socket(af, socktype, proto)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self._listen_addr, self._listen_port))
        server_socket.setblocking(False)
        self._server_sock = server_socket
        event_loop.add(self._server_sock,
                       eventloop.POLL_IN | eventloop.POLL_ERR, self)

    def close(self):
        self._server_sock.close()

    def set_msg_handler(self, msg_handler):
        self._msg_handler = msg_handler

    def _on_send_data(self, data, dest):
        if data and dest:
            logging.debug("UDPServer: send data %s to %s" % (data, dest))
            self._server_sock.sendto(data, dest)

    def _on_recv_data(self):
        data, addr = self._server_sock.recvfrom(BUF_SIZE)
        if data and addr:
            logging.debug("UDPServer: recved data %s from %s" % (data, addr))
            (msg_type, sequence_num), msg_body = struct.unpack(">BI", data[:5]), data[5:]
            if self._msg_handler is not None:
                messagehandler.handle_message(msg_type, msg_body, addr,
                                              self._msg_handler)
            else:
                logging.debug("UDPServer: no msg handler")

    def send_message(self, msg, to_addr):
        data = struct.pack(">BI", msg.message_type(), msg.sequence_number()) + msg.to_bytes();
        self._on_send_data(data, to_addr)

    def handle_event(self, sock, fd, event):
        if sock == self._server_sock:
            if event & eventloop.POLL_ERR:
                logging.error('UDP server_socket err')
            self._on_recv_data()
