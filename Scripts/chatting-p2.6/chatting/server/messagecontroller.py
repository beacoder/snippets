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


class MessageController(messagehandler.IMessageHandler):
    """Processing incomming messages."""

    def __init__(self, event_loop, msg_sender, msg_database):
        self._msg_sender = msg_sender
        self._db = msg_database
        self._event_loop = eventloop.EventLoop.default_loop()
        self._msg_sender.set_msg_handler(self)
        event_loop.add_periodic(self.handle_periodic)
        self._heartbeat_map = defaultdict(lambda: False)  # key: nick-name value: heartbeatreq_sent

    def handle_heartbeat_rsp(self, heartbeat_rsp, src_addr):
        client = self._db.get_client_name(src_addr)
        self._heartbeat_map[client] = False

    def handle_heartbeat_req_timeout(self, heartbeat_req, src_addr):
        client = self._db.get_client_name(src_addr)
        self._db.deactive_client(client)
        logging.info('MessageController: client is down')

    def handle_login_req(self, login_req, src_addr):
        logging.debug("received login req.")
        seq_num = login_req.sequence_number()
        if self._db.active_client(login_req.nick_name, src_addr):
            rsp = message.LoginRsp(seq_num, True, 'Sucess')
        else:
            rsp = message.LoginRsp(seq_num, False, 'Failure')
        self._msg_sender.send_message(rsp, src_addr)

    def handle_logout_req(self, logout_req, src_addr):
        logging.debug("received logout req.")
        seq_num = logout_req.sequence_number()
        if self._db.deactive_client(logout_req.nick_name, src_addr):
            rsp = message.LogoutRsp(seq_num, True, 'Sucess')
        else:
            rsp = message.LogoutRsp(seq_num, False, 'Failure')
        self._msg_sender.send_message(rsp, src_addr)

    def handle_chat_req(self, chat_req, src_addr):
        logging.debug("received chat request.")
        if self._db.is_client_online(address=src_addr):
            msg_to = chat_req.msg_to
            msg_content = chat_req.msg_content
            if self._db.is_client_online(name=msg_to):
                msg_from = self._db.get_client_name(src_addr)
                dest_addr = self._db.get_client_address(msg_to)
                chat_req = message.ChatReq(msg_from, msg_content)
                self._msg_sender.send_message(chat_req, dest_addr, src_addr)
            elif self._db.is_client_offline(msg_to):
                self._db.save_offline_msg(msg_to, msg_content)
            else:
                # msg_to is lost
                pass

    def handle_periodic(self):
        self._send_heartbeat()

    def _send_heartbeat(self):
        for client, address in self._db.get_online_clients().items():
            if not self._heartbeat_map[client]:
                self._msg_sender.send_message(message.HeartbeatReq(), address)
                self._heartbeat_map[client] = True
