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
from chatting import eventloop, message, messagehandler


BUF_SIZE = 65536
MAX_RETRY_TIMES = 3


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
        event_loop.add_periodic(self.handle_periodic)
        self._retransmission_map = {}  # key: seq_num value: retry-times
        self._msg_map = {}  # key: seq_num, value: msg

    def close(self):
        self._sock.close()

    def set_msg_handler(self, msg_handler):
        self._msg_handler = msg_handler

    def _on_recv_data(self):
        data, addr = self._sock.recvfrom(BUF_SIZE)
        if data and addr:
            logging.debug("UDPClient: recved data %s from %s" % (data, addr))
            (msg_type, seq_num), msg_body = struct.unpack(">BI", data[:5]), data[5:]
            if msg_type == message.HEARTBEAT_REQ:
                self.send_message(message.HeartbeatRsp(), False)
            elif seq_num in self._msg_map:  # cancel retransmission since Rsp is recved
                del self._msg_map[seq_num]
                del self._retransmission_map[seq_num]
                if self._msg_handler is not None:
                    messagehandler.handle_message(msg_type, msg_body, addr, self._msg_handler)
                else:
                    logging.debug("UDPClient: no msg handler")
            else:
                logging.warning("UDPClient: unexpected msg recved")

    def send_message(self, msg, retransmission=True):
        if retransmission:
            self._msg_map[msg.sequence_number()] = msg
            self._retransmission_map[msg.sequence_number()] = 0
        data = struct.pack(">BI", msg.message_type(), msg.sequence_number()) + msg.to_bytes();
        dest = (self._server_addr, self._server_port)
        if data and dest:
            logging.debug("UDPClient: send data %s to %s" % (data, dest))
            self._sock.sendto(data, dest)

    def handle_event(self, sock, fd, event):
        if sock == self._sock:
            if event & eventloop.POLL_ERR:
                logging.error('UDPClient socket error')
            self._on_recv_data()

    def handle_periodic(self):
        # message retransmission
        for seq_num, msg in self._msg_map.iteritems():
            if self._retransmission_map[seq_num] < MAX_RETRY_TIMES:
                self.send_message(msg)
                self._retransmission_map[seq_num] += 1
                logging.info('UDPClient: msg %s timeout for %d times' % (msg, self._retransmission_map[seq_num]))
            else:
                logging.warning('UDPClient: failed to send msg %s for %d times' % (msg, self._retransmission_map[seq_num]))
                if msg.message_type() == message.HEARTBEAT_REQ:
                    print("Server is down!")
                    sys.exit(1)
