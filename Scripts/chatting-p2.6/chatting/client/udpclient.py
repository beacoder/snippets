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
        self._heartbeatreq_sent = False
        self._heartbeatrsp_miss_times = 0

    def close(self):
        self._sock.close()

    def set_msg_handler(self, msg_handler):
        self._msg_handler = msg_handler

    def _handle_heartbeat_msg(self, msg_type):
        if msg_type == message.HEARTBEAT_REQ:
            # respond right away
            self.send_message(message.HeartbeatRsp())
        elif msg_type == message.HEARTBEAT_RSP:
            if not self._heartbeatreq_sent:
                logging.error("UDPClient: unexpected msg recved in _handle_heartbeat_msg")
                return
            if self._heartbeatrsp_miss_times <= MAX_RETRY_TIMES:
                self._heartbeatreq_sent = False
                self._heartbeatrsp_miss_times = 0
            else:
                logging.debug("UDPClient: too late, you should come early")
        else:
            pass

    def _on_send_data(self, data, dest):
        if data and dest:
            logging.debug("UDPClient: send data %s to %s" % (data, dest))
            self._sock.sendto(data, dest)

    def _on_recv_data(self):
        data, addr = self._sock.recvfrom(BUF_SIZE)
        if  data and addr:
            logging.debug("UDPClient: recved data %s from %s" % (data, addr))
            (msg_type,), msg_body = struct.unpack(">B", data[:1]), data[1:]
            if msg_type in (message.HEARTBEAT_REQ, message.HEARTBEAT_RSP):
                self._handle_heartbeat_msg(msg_type)
            elif self._msg_handler is not None:
                messagehandler.handle_message(msg_type, msg_body, addr, self._msg_handler)
            else:
                logging.debug("UDPClient: no msg handler")

    def send_message(self, msg):
        data = struct.pack(">B", msg.MSG_TYPE) + msg.to_bytes();
        self._on_send_data(data, (self._server_addr, self._server_port))

    def handle_event(self, sock, fd, event):
        if sock == self._sock:
            if event & eventloop.POLL_ERR:
                logging.error('UDPClient socket error')
            self._on_recv_data()

    def handle_periodic(self):
        if self._heartbeatreq_sent:
            if self._heartbeatrsp_miss_times < MAX_RETRY_TIMES:
                # try again
                self.send_message(message.HeartbeatReq())
                self._heartbeatrsp_miss_times += 1
                logging.info('UDPClient: heartbeat timeout for %d times', self._heartbeatrsp_miss_times)
            else:
                print("Server is down!")
                sys.exit(1)
        else:
            # send heartbeatreq every 10s
            self.send_message(message.HeartbeatReq())
            self._heartbeatreq_sent = True
