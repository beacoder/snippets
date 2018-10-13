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
        event_loop.add_periodic(self.handle_periodic)
        self._retransmission_map = {}  # key: (src_address, seq_num), value: retry-times
        self._msg_map = {}  # key: key: (src_address, seq_num), value: (msg, dest_addr)

    def close(self):
        self._server_sock.close()

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
        data, addr = self._server_sock.recvfrom(BUF_SIZE)
        if data and addr:
            logging.debug("UDPServer: recved data %s from %s" % (data, addr))
            message = unsearialize_message(data)
            msg_type, seq_num = message.message_type(), message.sequence_number()
            if msg_type == message.HEARTBEAT_REQ:  # handle incoming heartbeatreq
                self._handle_message(message, addr)
            else:
                map_key = (addr, seq_num)
                if map_key in self._msg_map:  # cancel retransmission if response is recved
                    del self._msg_map[map_key]
                    del self._retransmission_map[map_key]
                    self._handle_message(message, addr)
                else:
                    logging.error("UDPServer: unexpected message recved")

    def send_message(self, message, src_addr, dest_addr):
        if message.is_request(message):  # enable retransmission for requests only
            map_key = (src_addr, message.sequence_number())
            self._msg_map[map_key] = (message, dest_addr)
            self._retransmission_map[map_key] = 0
        data = searialize_message(message)
        if data and dest_addr:
            logging.debug("UDPServer: send data %s to %s" % (data, dest_addr))
            self._server_sock.sendto(data, dest_addr)

    def handle_event(self, sock, fd, event):
        if sock == self._server_sock:
            if event & eventloop.POLL_ERR:
                logging.error('UDP server_socket err')
            self._on_recv_data()

    def handle_periodic(self):
        # send heartbeat request
        # if not self._heartbeatreq_sent:
        #     self.send_message(message.HeartbeatReq())
        #     self._heartbeatreq_sent = True
        self.do_retransmission()

    def do_retransmission(self):
        for map_key, map_value in self._msg_map.iteritems():
            src_addr, _ = map_key
            msg, dest_addr = map_value
            if self._retransmission_map[map_key] < MAX_RETRY_TIMES:
                self.send_message(msg, src_addr, dest_addr)
                self._retransmission_map[map_key] += 1
                logging.info('UDPServer: msg %s timeout for %d times' % (msg, self._retransmission_map[map_key]))
            else:
                logging.warning('UDPServer: failed to send msg %s for %d times' % (msg, self._retransmission_map[map_key]))
