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


class MessageProcesser(messagehandler.IMessageHandler):
    """Processing incomming messages."""

    def __init__(self, msg_transceiver, msg_database):
        self._transceiver = msg_transceiver
        self._db = msg_database
        self._event_loop = eventloop.EventLoop.default_loop()
        self._transceiver.set_msg_handler(self)

    def handle_heartbeat_req(self, heartbeat_req, src_addr):
        logging.debug("received heartbeat req.")

    def handle_heartbeat_rsp(self, heartbeat_rsp, src_addr):
        logging.debug("received heartbeat rsp.")

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
