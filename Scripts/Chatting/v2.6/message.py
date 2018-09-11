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

import struct
import time
from enum import IntEnum, unique


@unique
class MessageType(IntEnum):
    """Message Type class."""

    INVALID_MSG = 0    # invalid message
    HEARTBEAT_REQ = 1  # heartbeat request
    LOGIN_REQ = 2      # login request
    LOGOUT_REQ = 3     # logout request
    HEARTBEAT_RSP = 4  # heartbeat response
    LOGIN_RSP = 5      # login response
    LOGOUT_RSP = 6     # logout response
    CHAT_MSG = 7       # one-to-one chat message
    BROADCAST_MSG = 8  # broadcast chat message


class IMessage:
    """Message interface."""

    def msg_type(self):
        raise NotImplementedError


class BaseMessage(IMessage):
    """Base message class."""

    def __init__(self):
        self._msg_type = MessageType(MessageType.INVALID_MSG)

    def msg_type(self):
        return self._msg_type


class HeartbeatReq(BaseMessage):
    """Represent a heartbeat request."""

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to
        self._msg_type = MessageType(MessageType.HEARTBEAT_REQ)


class LoginReq(BaseMessage):
    """Represent a login request."""

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to
        self._msg_type = MessageType(MessageType.LOGIN_REQ)


class LogoutReq(BaseMessage):
    """Represent a logout request."""

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to
        self._msg_type = MessageType(MessageType.LOGOUT_REQ)


class HeartbeatRsp(BaseMessage):
    """Represent a heartbeat response."""

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to
        self._msg_type = MessageType(MessageType.HEARTBEAT_RSP)


class LoginRsp(BaseMessage):
    """Represent a login response."""

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to
        self._msg_type = MessageType(MessageType.CHAT_MSG)


class LogoutRsp(BaseMessage):
    """Represent a logout response."""

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to
        self._msg_type = MessageType(MessageType.CHAT_MSG)


class ChatMessage(BaseMessage):
    """Represent a single chat message."""

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to
        self._msg_type = MessageType(MessageType.CHAT_MSG)


class BroadcastMessage(BaseMessage):
    """Represent a broadcast chat message."""

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to
        self._msg_type = MessageType(MessageType.CHAT_MSG)
