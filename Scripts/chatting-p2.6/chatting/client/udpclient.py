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
        self._retransmission_map = {}  # key: seq_num, value: retry-times
        self._msg_map = {}  # key: seq_num, value: msg
        self._heartbeatreq_sent = False

    def close(self):
        self._sock.close()

    def set_msg_handler(self, msg_handler):
        self._msg_handler = msg_handler

    def _handle_message(message, from_addr):
        msg_handler = self._msg_handler
        msg_type = message.message_type()
        if msg_handler:
            if msg_type == message.HEARTBEAT_REQ:
                msg_handler.handle_heartbeat_req(message, from_addr)
            elif msg_type == message.HEARTBEAT_RSP:
                msg_handler.handle_heartbeat_rsp(message, from_addr)
            elif msg_type == message.LOGIN_REQ:
                msg_handler.handle_login_req(message, from_addr)
            elif msg_type == message.LOGIN_RSP:
                msg_handler.handle_login_rsp(message, from_addr)
            elif msg_type == message.LOGOUT_REQ:
                msg_handler.handle_logout_req(message, from_addr)
            elif msg_type == message.LOGOUT_RSP:
                msg_handler.handle_logout_rsp(message, from_addr)
            elif msg_type == message.CHAT_MSG:
                msg_handler.handle_chat_msg(message, from_addr)
            elif msg_type == message.BROADCAST_MSG:
                msg_handler.handle_broadcast_msg(message, from_addr)
            else:
                raise ValueError("Invalid message type: %d" % msg_type)

    def _on_recv_data(self):
        data, addr = self._sock.recvfrom(BUF_SIZE)
        if data and addr:
            logging.debug("UDPClient: recved data %s from %s" % (data, addr))
            message = unsearialize_message(data)
            msg_type, seq_num = message.message_type(), message.sequence_number()
            if msg_type == message.HEARTBEAT_REQ:  # handle incoming heartbeatreq
                self._handle_message(message, addr)
            else:
                if seq_num in self._msg_map:  # cancel retransmission if response is recved
                    del self._msg_map[seq_num]
                    del self._retransmission_map[seq_num]
                    if msg_type == message.HEARTBEAT_RSP:
                        self._heartbeatreq_sent = False  # start sending heartbeatreq again
                    else:
                        self._handle_message(message, addr)
                else:
                    logging.error("UDPClient: unexpected message recved")

    def send_message(self, msg):
        if message.is_request(msg):  # enable retransmission for requests only
            self._msg_map[msg.sequence_number()] = msg
            self._retransmission_map[msg.sequence_number()] = 0
        data = searialize_message(message)
        dest = (self._server_addr, self._server_port)
        if data and dest:
            logging.debug("UDPClient: send data %s to %s" % (data, dest))
            self._sock.sendto(data, dest)

    def handle_event(self, sock, fd, event):
        if sock == self._sock:
            if event & eventloop.POLL_ERR:
                logging.error('UDPClient socket error')
            self._on_recv_data()

    def do_retransmission(self):
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

    def handle_periodic(self):
        # send heartbeat request
        if not self._heartbeatreq_sent:
            self.send_message(message.HeartbeatReq())
            self._heartbeatreq_sent = True
        self.do_retransmission()
