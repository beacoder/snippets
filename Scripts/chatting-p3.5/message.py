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
    CHAT_MSG_REQ = 7   # one-to-one chat message
    CHAT_MSG_RSP = 8   # response to chat message
    BROADCAST_MSG = 9  # broadcast chat message


class IMessage:
    """Message interface."""

    MSG_TYPE = MessageType.INVALID_MSG
    ENCODE_FORMAT = None

    def to_bytes(self):
        raise NotImplementedError


class HeartbeatReq(IMessage):
    """Represent a heartbeat request."""

    MSG_TYPE = MessageType.HEARTBEAT_REQ
    ENCODE_FORMAT = ">II"

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to

    def to_bytes(self):
        return struct.pack(HeartbeatReq.ENCODE_FORMAT, self._from, self._to)


class LoginReq(IMessage):
    """Represent a login request."""

    MSG_TYPE = MessageType.LOGIN_REQ
    ENCODE_FORMAT = ">II"

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to

    def to_bytes(self):
        return struct.pack(LoginReq.ENCODE_FORMAT, self._from, self._to)


class LogoutReq(IMessage):
    """Represent a logout request."""

    MSG_TYPE = MessageType.LOGOUT_REQ
    ENCODE_FORMAT = ">II"

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to

    def to_bytes(self):
        return struct.pack(LogoutReq.ENCODE_FORMAT, self._from, self._to)


class HeartbeatRsp(IMessage):
    """Represent a heartbeat response."""

    MSG_TYPE = MessageType.HEARTBEAT_RSP
    ENCODE_FORMAT = ">II"

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to

    def to_bytes(self):
        return struct.pack(HeartbeatRsp.ENCODE_FORMAT, self._from, self._to)


class LoginRsp(IMessage):
    """Represent a login response."""

    MSG_TYPE = MessageType.LOGIN_RSP
    ENCODE_FORMAT = ">II"

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to

    def to_bytes(self):
        return struct.pack(LoginRsp.ENCODE_FORMAT, self._from, self._to)


class LogoutRsp(IMessage):
    """Represent a logout response."""

    MSG_TYPE = MessageType.LOGOUT_RSP
    ENCODE_FORMAT = ">II"

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to

    def to_bytes(self):
        return struct.pack(LogoutRsp.ENCODE_FORMAT, self._from, self._to)


class ChatMessage(IMessage):
    """Represent a single chat message."""

    MSG_TYPE = MessageType.CHAT_MSG_REQ
    ENCODE_FORMAT = ">II"

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to

    def to_bytes(self):
        return struct.pack(ChatMessage.ENCODE_FORMAT, self._from, self._to)


class BroadcastMessage(IMessage):
    """Represent a broadcast chat message."""

    MSG_TYPE = MessageType.BROADCAST_MSG
    ENCODE_FORMAT = ">II"

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to

    def to_bytes(self):
        return struct.pack(BroadcastMessage.ENCODE_FORMAT, self._from, self._to)


def create_message(msg_type, msg_body):
    """Factory method for message class."""

    if msg_type == MessageType.HEARTBEAT_REQ:
        data = struct.unpack(HeartbeatReq.ENCODE_FORMAT, msg_body)
        return HeartbeatReq(*data) # unpack tuple into *args.
    elif msg_type == MessageType.BROADCAST_MSG:
        data = struct.unpack(LoginReq.ENCODE_FORMAT, msg_body)
        return LoginReq(*data)
    elif msg_type == MessageType.CHAT_MSG_REQ:
        data = struct.unpack(ChatMessage.ENCODE_FORMAT, msg_body)
        return ChatMessage(*data)
    else:
        raise ValueError
