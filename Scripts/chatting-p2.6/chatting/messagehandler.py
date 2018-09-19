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
        self._msg_sender = msg_sender
        self._msg_database = msg_database
        self._event_loop = eventloop.EventLoop.default_loop()

    def handle_heartbeat_req(self, heartbeat_req, from_addr):
        pass

    def handle_heartbeat_rsp(self, heartbeat_rsp, from_addr):
        pass

    def handle_login_req(self, login_req, from_addr):
        ret = self._msg_database.active_client(login_req.nick_name, from_addr)
        rsp = LoginRsp(ret, b"Sucess") if ret else LoginRsp(ret, b"Failure")
        self._msg_sender(rsp, from_addr)

    def handle_login_rsp(self, login_rsp, from_addr):
        pass

    def handle_logout_req(self, logout_req, from_addr):
        ret = self._msg_database.deactive_client(logout_req.nick_name, from_addr)
        rsp = LogoutRsp(ret, b"Sucess") if ret else LogoutRsp(ret, b"Failure")
        self._msg_sender(rsp, from_addr)

    def handle_logout_rsp(self, logout_rsp, from_addr):
        pass

    def handle_chat_msg(self, chat_msg, from_addr):
        if self._msg_database.is_client_active(address=from_addr):
            peer_client = chat_msg.msg_to
            msg_content = chat_msg.msg_content
            if self._msg_database.is_client_active(name=peer_client):
                # forward msg_content to peer_client through msg_sender
                pass
            elif self._msg_database.is_client_offline(peer_client):
                # save msg_content as offline message for peer_client
                pass
            else:
                # peer_client is lost
                pass

    def handle_broadcast_msg(self, broadcast_msg, from_addr):
        pass
