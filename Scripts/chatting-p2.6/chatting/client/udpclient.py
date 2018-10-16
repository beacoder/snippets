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
        self._retry_map = {}  # key: seq_num, value: retry-times
        self._msg_map = {}    # key: seq_num, value: msg
        self._heartbeatreq_sent = False

    def close(self):
        self._sock.close()

    def set_msg_handler(self, msg_handler):
        self._msg_handler = msg_handler

    def _handle_response(self, msg, from_addr):
        msg_handler = self._msg_handler
        msg_type = msg.message_type()
        if msg_handler:
            if msg_type == message.HEARTBEAT_RSP:
                self._heartbeatreq_sent = False
            elif msg_type == message.LOGIN_RSP:
                msg_handler.handle_login_rsp(msg, from_addr)
            elif msg_type == message.LOGOUT_RSP:
                msg_handler.handle_logout_rsp(msg, from_addr)
            elif msg_type == message.CHAT_RSP:
                pass
            else:
                raise ValueError("Invalid message type: %d" % msg_type)

    def _handle_request(self, msg, from_addr):
        msg_handler = self._msg_handler
        msg_type = msg.message_type()
        seq_num = msg.sequence_number()
        if msg_handler:
            if msg_type == message.HEARTBEAT_REQ:
                self.send_message(message.HeartbeatRsp(seq_num))
            elif msg_type == message.LOGIN_REQ:
                msg_handler.handle_login_req(msg, from_addr)
            elif msg_type == message.LOGOUT_REQ:
                msg_handler.handle_logout_req(msg, from_addr)
            elif msg_type == message.CHAT_REQ:
                self.send_message(message.ChatRsp(seq_num, True, 'Sucess'))
                msg_handler.handle_chat_req(msg, from_addr)
            else:
                raise ValueError("Invalid message type: %d" % msg_type)

    def _on_recv_data(self):
        data, addr = self._sock.recvfrom(BUF_SIZE)
        if data and addr:
            logging.debug("UDPClient: recved data %s from %s" % (data, addr))
            msg = message.desearialize_message(data)
            msg_type, seq_num = msg.message_type(), msg.sequence_number()
            if message.is_request(msg):
                self._handle_request(msg, addr)
            elif message.is_response(msg):
                if seq_num in self._msg_map:
                    del self._msg_map[seq_num]
                    del self._retry_map[seq_num]
                    self._handle_response(msg, addr)
                else:
                    logging.error("UDPClient: unexpected message recved")

    def send_message(self, msg):
        if message.is_request(msg):
            if msg.sequence_number() not in self._msg_map:
                self._msg_map[seq_num] = msg
                self._retry_map[seq_num] = 0
        data = message.searialize_message(msg)
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
        self._send_heartbeat()
        self._do_retransmission()

    def _send_heartbeat(self):
        if not self._heartbeatreq_sent:
            self.send_message(message.HeartbeatReq())
            self._heartbeatreq_sent = True

    def _do_retransmission(self):
        for seq_num, msg in self._msg_map.iteritems():
            if self._retry_map[seq_num] < MAX_RETRY_TIMES:
                self.send_message(msg)
                self._retry_map[seq_num] += 1
                logging.info('UDPClient: msg %s timeout for %d times' % (msg, self._retry_map[seq_num]))
            else:
                logging.warning('UDPClient: failed to send msg %s for %d times' % (msg, self._retry_map[seq_num]))
                if msg.message_type() == message.HEARTBEAT_REQ:
                    print("Server is down!")
                    sys.exit(1)
