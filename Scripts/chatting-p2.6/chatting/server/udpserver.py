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
        self._msg_map = {}  # key: key: (src_address, seq_num), value: msg

    def close(self):
        self._server_sock.close()

    def set_msg_handler(self, msg_handler):
        self._msg_handler = msg_handler

    def _on_recv_data(self):
        data, addr = self._server_sock.recvfrom(BUF_SIZE)
        if data and addr:
            logging.debug("UDPServer: recved data %s from %s" % (data, addr))
            (msg_type, seq_num), msg_body = struct.unpack(">BI", data[:5]), data[5:]
            if msg_type == message.HEARTBEAT_REQ:  # handle incoming heartbeatreq
                if self._msg_handler:
                    messagehandler.handle_message(msg_type, msg_body, addr, self._msg_handler)
            else:
                map_key = (addr, seq_num)
                if map_key in self._msg_map:  # cancel retransmission if response is recved
                    del self._msg_map[map_key]
                    del self._retransmission_map[map_key]
                    if self._msg_handler:
                        messagehandler.handle_message(msg_type, msg_body, addr, self._msg_handler)
                else:
                    logging.error("UDPServer: unexpected message recved")

    def send_message(self, msg, src_addr, dest_addr):
        if message.is_request(msg):  # enable retransmission for requests only
            map_key = (src_addr, msg.sequence_number())
            self._msg_map[map_key] = msg
            self._retransmission_map[map_key] = 0
        data = struct.pack(">BI", msg.message_type(), msg.sequence_number()) + msg.to_bytes();
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
        for seq_num, msg in self._msg_map.iteritems():
            if self._retransmission_map[seq_num] < MAX_RETRY_TIMES:
                self.send_message(msg)
                self._retransmission_map[seq_num] += 1
                logging.info('UDPServer: msg %s timeout for %d times' % (msg, self._retransmission_map[seq_num]))
            else:
                logging.warning('UDPServer: failed to send msg %s for %d times' % (msg, self._retransmission_map[seq_num]))
