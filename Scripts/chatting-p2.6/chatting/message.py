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


INVALID_MSG = 0    # invalid message
HEARTBEAT_REQ = 1  # heartbeat request
HEARTBEAT_RSP = 2  # heartbeat response
LOGIN_REQ = 3      # login request
LOGIN_RSP = 4      # login response
LOGOUT_REQ = 5     # logout request
LOGOUT_RSP = 6     # logout response
CHAT_MSG = 7       # one-to-one chat message
BROADCAST_MSG = 8  # broadcast chat message


def unpack_helper(fmt, data):
    size = struct.calcsize(fmt)
    return struct.unpack(fmt, data[:size]), data[size:]


class IMessage(object):
    """Message interface."""

    MSG_TYPE = INVALID_MSG
    ENCODE_FORMAT = None  # use fixed-length for now, change to TLV if needed.

    def to_bytes(self):
        raise NotImplementedError

    def from_bytes(self, data):
        raise NotImplementedError


class HeartbeatReq(IMessage):
    """Represent a heartbeat request."""

    MSG_TYPE = HEARTBEAT_REQ
    ENCODE_FORMAT = "15s"  # 15s -> "HeartbeatReq"

    def __init__(self):
        self._msg = b"HeartbeatReq"

    def to_bytes(self):
        return struct.pack(HeartbeatReq.ENCODE_FORMAT, self._msg)

    def from_bytes(self, data):
        (self._msg,), _ =  unpack_helper(HeartbeatReq.ENCODE_FORMAT, data)
        return self


class HeartbeatRsp(IMessage):
    """Represent a heartbeat response."""

    MSG_TYPE = HEARTBEAT_RSP
    ENCODE_FORMAT = "15s"  # 15s -> "HeartbeatRsp"

    def __init__(self):
        self._msg = b"HeartbeatRsp"

    def to_bytes(self):
        return struct.pack(HeartbeatRsp.ENCODE_FORMAT, self._msg)

    def from_bytes(self, data):
        (self._msg,), _ =  unpack_helper(HeartbeatRsp.ENCODE_FORMAT, data)
        return self


class LoginReq(IMessage):
    """Represent a login request."""

    MSG_TYPE = LOGIN_REQ
    ENCODE_FORMAT = "30s"  # nick-name

    def __init__(self, nick_name = None):
        self._nick_name = nick_name

    def to_bytes(self):
        return struct.pack(LoginReq.ENCODE_FORMAT, self._nick_name)

    def from_bytes(self, data):
        (self._nick_name,), _ =  unpack_helper(LoginReq.ENCODE_FORMAT, data)
        return self


class LogoutReq(IMessage):
    """Represent a logout request."""

    MSG_TYPE = LOGOUT_REQ
    ENCODE_FORMAT = "30s"  # nick-name

    def __init__(self, nick_name = None):
        self._nick_name = nick_name

    def to_bytes(self):
        return struct.pack(LogoutReq.ENCODE_FORMAT, self._nick_name)

    def from_bytes(self, data):
        (self._nick_name,), _ =  unpack_helper(LogoutReq.ENCODE_FORMAT, data)
        return self


class LoginRsp(IMessage):
    """Represent a login response."""

    MSG_TYPE = LOGIN_RSP
    ENCODE_FORMAT = "?10s"  # ? -> LoginResult, 10s -> Reason

    def __init__(self, result = None, reason = None):
        self._result = result
        self._reason = reason

    def to_bytes(self):
        return struct.pack(LoginRsp.ENCODE_FORMAT, self._result, self._reason)

    def from_bytes(self, data):
        (self._result,), data =  unpack_helper("?", data)
        (self._reason,), _ =  unpack_helper("10s", data)
        return self


class LogoutRsp(IMessage):
    """Represent a logout response."""

    MSG_TYPE = LOGOUT_RSP
    ENCODE_FORMAT = "?10s"  # ? -> LogoutResult, 10s -> Reason

    def __init__(self, result = None, reason = None):
        self._result = result
        self._reason = reason

    def to_bytes(self):
        return struct.pack(LogoutRsp.ENCODE_FORMAT, self._result, self._reason)

    def from_bytes(self, data):
        (self._result,), data =  unpack_helper("?", data)
        (self._reason,), _ =  unpack_helper("10s", data)
        return self


class ChatMessage(IMessage):
    """Represent a single chat message."""

    MSG_TYPE = CHAT_MSG
    ENCODE_FORMAT = "30s1024s"  # 30s -> receiver's nick-name, 1024s -> chat-msg

    def __init__(self, msg_to = None, msg = None):
        self._msg_to = msg
        self._msg = msg

    def to_bytes(self):
        return struct.pack(ChatMessage.ENCODE_FORMAT, self._msg_to, self._msg)

    def from_bytes(self, data):
        (self._msg_to,), data = unpack_helper("30s", data)
        (self._msg,), _ = unpack_helper("1024s", data)
        return self


class BroadcastMessage(IMessage):
    """Represent a broadcast chat message."""

    MSG_TYPE = BROADCAST_MSG
    ENCODE_FORMAT = "II"  # TODO: elaborate this later

    def __init__(self, msg_from, msg_to):
        self._from = msg_from
        self._to = msg_to

    def to_bytes(self):
        return struct.pack(BroadcastMessage.ENCODE_FORMAT, self._from, self._to)


def create_message(msg_type, msg_body):
    """Factory method for message class."""

    if msg_type == HEARTBEAT_REQ:
        return HeartbeatReq().from_bytes(msg_body)
    elif msg_type == HEARTBEAT_RSP:
        return HeartbeatRsp().from_bytes(msg_body)
    if msg_type == LOGIN_REQ:
        return LoginReq().from_bytes(msg_body)
    elif msg_type == LOGIN_RSP:
        return LoginRsp().from_bytes(msg_body)
    if msg_type == LOGOUT_REQ:
        return LogoutReq().from_bytes(msg_body)
    elif msg_type == LOGOUT_RSP:
        return LogoutRsp().from_bytes(msg_body)
    elif msg_type == CHAT_MSG:
        return ChatMessage().from_bytes(msg_body)
    elif msg_type == BROADCAST_MSG:
        return BroadcastMessage().from_bytes(msg_body)
    else:
        raise ValueError
