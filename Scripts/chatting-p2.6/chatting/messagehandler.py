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

from . import message


class IMessageHandler(object):
    """Message handler interface."""

    def handle_heartbeat_req(self, heartbeat_req, src_addr):
        raise NotImplementedError

    def handle_heartbeat_rsp(self, heartbeat_rsp, src_addr):
        raise NotImplementedError

    def handle_login_req(self, login_req, src_addr):
        raise NotImplementedError

    def handle_login_rsp(self, login_rsp, src_addr):
        raise NotImplementedError

    def handle_logout_req(self, logout_req, src_addr):
        raise NotImplementedError

    def handle_logout_rsp(self, logout_rsp, src_addr):
        raise NotImplementedError

    def handle_chat_msg(self, chat_msg, src_addr):
        raise NotImplementedError

    def handle_broadcast_msg(self, broadcast_msg, src_addr):
        raise NotImplementedError


def handle_message(msg_type, msg_body, from_addr, msg_handler):
    try:
        if msg_type == HEARTBEAT_REQ:
            msg = HeartbeatReq().from_bytes(msg_body)
            msg_handler.handle_heartbeat_req(msg, from_addr)
        elif msg_type == HEARTBEAT_RSP:
            msg = HeartbeatRsp().from_bytes(msg_body)
            msg_handler.handle_heartbeat_rsp(msg, from_addr)
        if msg_type == LOGIN_REQ:
            msg = LoginReq().from_bytes(msg_body)
            msg_handler.handle_login_req(msg, from_addr)
        elif msg_type == LOGIN_RSP:
            msg =  LoginRsp().from_bytes(msg_body)
            msg_handler.handle_login_rsp(msg, from_addr)
        if msg_type == LOGOUT_REQ:
            msg = LogoutReq().from_bytes(msg_body)
            msg_handler.handle_logout_req(msg, from_addr)
        elif msg_type == LOGOUT_RSP:
            msg = LogoutRsp().from_bytes(msg_body)
            msg_handler.handle_logout_rsp(msg, from_addr)
        elif msg_type == CHAT_MSG:
            msg = ChatMessage().from_bytes(msg_body)
            msg_handler.handle_chat_msg(msg, from_addr)
        elif msg_type == BROADCAST_MSG:
            msg = BroadcastMessage().from_bytes(msg_body)
            msg_handler.handle_broadcast_msg(msg, from_addr)
        else:
            raise ValueError
    except Exception as e:
        print_exception(e)
        # sys.exit(1)
