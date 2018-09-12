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
import time


class IMessageHandler:
    """Message Handler interface."""

    def handle_heartbeat_req(self, heartbeat_req):
        raise NotImplementedError

    def handle_login_req(self, login_req):
        raise NotImplementedError

    def handle_logout_req(self, logout_req):
        raise NotImplementedError

    def handle_heartbeat_rsp(self, heartbeat_rsp):
        raise NotImplementedError

    def handle_login_rsp(self, login_rsp):
        raise NotImplementedError

    def handle_logout_rsp(self, logout_rsp):
        raise NotImplementedError

    def handle_chat_msg(self, chat_msg):
        raise NotImplementedError

    def handle_broadcast_msg(self, broadcast_msg):
        raise NotImplementedError


class MessageHandler(IMessageHandler):
    """Message Handler class."""

    def handle_heartbeat_req(self, heartbeat_req):
        pass

    def handle_login_req(self, login_req):
        pass

    def handle_logout_req(self, logout_req):
        pass

    def handle_heartbeat_rsp(self, heartbeat_rsp):
        pass

    def handle_login_rsp(self, login_rsp):
        pass

    def handle_logout_rsp(self, logout_rsp):
        pass

    def handle_chat_msg(self, chat_msg):
        pass

    def handle_broadcast_msg(self, broadcast_msg):
        pass