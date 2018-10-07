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
from chatting import eventloop, message, messagehandler
from collections import defaultdict


MAX_RETRY_TIMES = 3


class MessageProcesser(messagehandler.IMessageHandler):
    """Processing incomming messages."""

    def __init__(self, event_loop, msg_transceiver, msg_database):
        self._transceiver = msg_transceiver
        self._db = msg_database
        self._event_loop = eventloop.EventLoop.default_loop()
        self._transceiver.set_msg_handler(self)
        event_loop.add_periodic(self.handle_periodic)
        self._heartbeat_map = defaultdict(lambda: [False, 0])  # key: nick-name value: [heartbeatreq_sent, heartbeatrsp_miss_times]

    def handle_heartbeat_req(self, heartbeat_req, src_addr):
        # respond right away
        self._transceiver.send_message(message.HeartbeatRsp(), src_addr)

    def handle_heartbeat_rsp(self, heartbeat_rsp, src_addr):
        msg_from = self._db.get_client_name(src_addr)
        if msg_from is None:
            logging.warning("MessageProcesser: unregistered ip-address")
        else:
            heartbeatreq_sent, heartbeatrsp_miss_times = self._heartbeat_map[msg_from]
            if not heartbeatreq_sent:
                logging.warning("MessageProcesser: unexpected heartbeat_rsp recved")
            else:
                if heartbeatrsp_miss_times <= MAX_RETRY_TIMES:
                    heartbeatreq_sent, heartbeatrsp_miss_times = [False, 0]
                    self._heartbeat_map[msg_from] = [heartbeatreq_sent,
                                                     heartbeatrsp_miss_times]
                else:
                    logging.warning("MessageProcesser: too late, you should come early")

    def handle_login_req(self, login_req, src_addr):
        logging.debug("received login req.")
        ret = self._db.active_client(login_req.nick_name, src_addr)
        rsp = message.LoginRsp(ret, b"Sucess") if ret else message.LoginRsp(ret, b"Failure")
        self._transceiver.send_message(rsp, src_addr)

    def handle_logout_req(self, logout_req, src_addr):
        logging.debug("received logout req.")
        ret = self._db.deactive_client(logout_req.nick_name, src_addr)
        rsp = message.LogoutRsp(ret, b"Sucess") if ret else LogoutRsp(ret, b"Failure")
        self._transceiver.send_message(rsp, src_addr)

    def handle_chat_msg(self, chat_msg, src_addr):
        logging.debug("received chat msg.")
        if self._db.is_client_online(address=src_addr):
            msg_to = chat_msg.msg_to
            msg_content = chat_msg.msg_content
            if self._db.is_client_online(name=msg_to):
                msg_from = self._db.get_client_name(src_addr)
                dest_addr = self._db.get_client_address(msg_to)
                chat_msg = message.ChatMessage(msg_from, msg_content)
                self._transceiver.send_message(chat_msg, dest_addr)
            elif self._db.is_client_offline(msg_to):
                self._db.save_offline_msg(msg_to, msg_content)
            else:
                # msg_to is lost
                pass

    def handle_broadcast_msg(self, broadcast_msg, src_addr):
        logging.debug("received broadcast msg.")

    def handle_periodic(self):
        lost_clients = set()
        for client, address in self._db.get_online_clients().items():
            heartbeatreq_sent, heartbeatrsp_miss_times = self._heartbeat_map[client]
            if heartbeatreq_sent:
                if heartbeatrsp_miss_times < MAX_RETRY_TIMES:
                    # try again
                    self._transceiver.send_message(message.HeartbeatReq(), address)
                    self._heartbeat_map[client][1] += 1
                    logging.info('MessageProcesser: heartbeat timeout for %d times',
                                 self._heartbeat_map[client][1])
                else:
                    logging.info('MessageProcesser: client is down')
                    lost_clients.add(client)
            else:
                # for each client, send heartbeatreq every 10s
                self._transceiver.send_message(message.HeartbeatReq(), address)
                heartbeatreq_sent, heartbeatrsp_miss_times = [True, 0]
                self._heartbeat_map[client] = [heartbeatreq_sent,
                                               heartbeatrsp_miss_times]
         # deactive offline clients
        for client in lost_clients:
            self._db.deactive_client(client)
