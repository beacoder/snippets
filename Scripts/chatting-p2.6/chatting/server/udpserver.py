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
MAX_RETRY_TIMES = 3


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
        event_loop.add_periodic(self.handle_periodic)
        self._retry_map = {}  # key: seq_num, value: retry-times
        self._msg_map = {}    # key: seq_num, value: (msg, dest_addr)

    def close(self):
        self._server_sock.close()

    def set_msg_handler(self, msg_handler):
        self._msg_handler = msg_handler

    def _handle_response(self, msg, from_addr):
        msg_handler = self._msg_handler
        msg_type = msg.message_type()
        if msg_handler:
            if msg_type == message.HEARTBEAT_RSP:
                msg_handler.handle_heartbeat_rsp(msg, from_addr)
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
                self.send_message(message.HeartbeatRsp(seq_num), from_addr)
            elif msg_type == message.LOGIN_REQ:
                msg_handler.handle_login_req(msg, from_addr)
            elif msg_type == message.LOGOUT_REQ:
                msg_handler.handle_logout_req(msg, from_addr)
            elif msg_type == message.CHAT_REQ:
                self.send_message(message.ChatRsp(seq_num, 'Sucess', ''), from_addr)
                msg_handler.handle_chat_req(msg, from_addr)
            else:
                raise ValueError("Invalid message type: %d" % msg_type)

    def _cancel_retransmission(seq_num):
        del self._msg_map[seq_num]
        del self._retry_map[seq_num]

    def _on_recv_data(self):
        data, addr = self._server_sock.recvfrom(BUF_SIZE)
        if data and addr:
            logging.debug("UDPServer: recved data %s from %s" % (data, addr))
            msg = message.desearialize_message(data)
            seq_num = msg.sequence_number()
            if message.is_request(msg):
                self._handle_request(msg, addr)
            elif message.is_response(msg):
                if seq_num in self._msg_map:
                    _cancel_retransmission(seq_num)
                    self._handle_response(msg, addr)
                else:
                    logging.error("UDPServer: unexpected message recved")

    def send_message(self, msg, dest_addr):
        if message.is_request(msg):
            seq_num = msg.sequence_number()
            if seq_num not in self._msg_map:
                self._msg_map[seq_num] = (msg, dest_addr)
                self._retry_map[seq_num] = 0
        data = message.searialize_message(msg)
        if data and dest_addr:
            logging.debug("UDPServer: send data %s to %s" % (data, dest_addr))
            self._server_sock.sendto(data, dest_addr)

    def handle_event(self, sock, fd, event):
        if sock == self._server_sock:
            if event & eventloop.POLL_ERR:
                logging.error('UDP server_socket err')
            self._on_recv_data()

    def handle_periodic(self):
        self._do_retransmission()

    def _do_retransmission(self):
        for seq_num, (msg, dest_addr) in self._msg_map.iteritems():
            if self._retry_map[seq_num] < MAX_RETRY_TIMES:
                self.send_message(msg, dest_addr)
                self._retry_map[seq_num] += 1
                logging.info('UDPServer: msg %s timeout for %d times' % (msg, self._retry_map[seq_num]))
            else:
                _cancel_retransmission(seq_num)
                logging.warning('UDPServer: failed to send msg %s for %d times' % (msg, self._retry_map[seq_num]))
                if msg.message_type() == message.HEARTBEAT_REQ:
                    self._msg_handler.handle_heartbeat_req_timeout(msg, dest_addr)
