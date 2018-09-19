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


class IMessageSender:
    """Message sender interface."""

    def send_message(self, msg, to_addr):
        raise NotImplementedError


class IMessageReceiver:
    """Message receiver interface."""

    def recv_message(self, msg, from_addr):
        raise NotImplementedError


class MessageReceiver(IMessageReceiver):
    """Receiving incomming messages."""

    # TODO: merge create_message logic into this class.

    def __init__(self, msg_handler):
        self._msg_handler = msg_handler

    def recv_message(self, msg, from_addr):
        if msg.MSG_TYPE == HEARTBEAT_REQ:
            self._msg_handler.handle_heartbeat_req(msg, from_addr)
        elif msg.MSG_TYPE == HEARTBEAT_RSP:
            self._msg_handler.handle_heartbeat_rsp(msg, from_addr)
        if msg.MSG_TYPE == LOGIN_REQ:
            self._msg_handler.handle_login_req(msg, from_addr)
        elif msg.MSG_TYPE == LOGIN_RSP:
            self._msg_handler.handle_login_rsp(msg, from_addr)
        if msg.MSG_TYPE == LOGOUT_REQ:
            self._msg_handler.handle_logout_req(msg, from_addr)
        elif msg.MSG_TYPE == LOGOUT_RSP:
            self._msg_handler.handle_logout_rsp(msg, from_addr)
        elif msg.MSG_TYPE == CHAT_MSG:
            self._msg_handler.handle_chat_msg(msg, from_addr)
        elif msg.MSG_TYPE == BROADCAST_MSG:
            self._msg_handler.handle_broadcast_msg(msg, from_addr)
        else:
            raise ValueError
