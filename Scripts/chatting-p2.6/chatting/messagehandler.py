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

import message
import messagereceiver
import eventloop


class MessageHandler(object):
    """Processing incomming messages."""

    def __init__(self, msg_sender, msg_database):
        self._sender = msg_sender
        self._db = msg_database
        self._event_loop = eventloop.EventLoop.default_loop()

    def handle_heartbeat_req(self, heartbeat_req, src_addr):
        pass

    def handle_heartbeat_rsp(self, heartbeat_rsp, src_addr):
        pass

    def handle_login_req(self, login_req, src_addr):
        ret = self._db.active_client(login_req.nick_name, src_addr)
        rsp = LoginRsp(ret, b"Sucess") if ret else LoginRsp(ret, b"Failure")
        self._sender(rsp, src_addr)

    def handle_login_rsp(self, login_rsp, src_addr):
        pass

    def handle_logout_req(self, logout_req, src_addr):
        ret = self._db.deactive_client(logout_req.nick_name, src_addr)
        rsp = LogoutRsp(ret, b"Sucess") if ret else LogoutRsp(ret, b"Failure")
        self._sender(rsp, src_addr)

    def handle_logout_rsp(self, logout_rsp, src_addr):
        pass

    def handle_chat_msg(self, chat_msg, src_addr):
        if self._db.is_client_online(address=src_addr):
            msg_to = chat_msg.msg_to
            msg_content = chat_msg.msg_content
            if self._db.is_client_online(name=msg_to):
                msg_from = self._db.get_client_name(src_addr)
                dest_addr = self._db.get_client_address(msg_to)
                self._sender(ChatMessage(msg_from, msg_content), dest_addr)
            elif self._db.is_client_offline(msg_to):
                self._db.save_offline_msg(msg_to, msg_content)
            else:
                # msg_to is lost
                pass

    def handle_broadcast_msg(self, broadcast_msg, src_addr):
        pass
