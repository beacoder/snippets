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

import struct
import time


__all__ = ['HeartbeatReq', 'HeartbeatRsp', 'LoginReq', 'LoginRsp',
           'LogoutReq', 'LogoutRsp', 'ChatMessage', 'BroadcastMessage',
           'INVALID_MSG', 'HEARTBEAT_REQ', 'HEARTBEAT_RSP', 'LOGIN_REQ',
           'LOGIN_RSP', 'LOGOUT_REQ', 'LOGOUT_RSP', 'CHAT_MSG', 'BROADCAST_MSG']

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

    def __repr__(self):
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

    def __repr__(self):
        return "HeartbeatReq"


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

    def __repr__(self):
        return "HeartbeatRsp"


class LoginReq(IMessage):
    """Represent a login request."""

    MSG_TYPE = LOGIN_REQ
    ENCODE_FORMAT = "30s"  # nick-name

    def __init__(self, nick_name=None):
        self.nick_name = nick_name

    def to_bytes(self):
        return struct.pack(LoginReq.ENCODE_FORMAT, self.nick_name)

    def from_bytes(self, data):
        (self.nick_name,), _ =  unpack_helper(LoginReq.ENCODE_FORMAT, data)
        return self

    def __repr__(self):
        return "nick-name: %s" % self.nick_name


class LoginRsp(IMessage):
    """Represent a login response."""

    MSG_TYPE = LOGIN_RSP
    ENCODE_FORMAT = "?10s"  # ? -> LoginResult, 10s -> Reason

    def __init__(self, result=None, reason=None):
        self.result = result
        self.reason = reason

    def to_bytes(self):
        return struct.pack(LoginRsp.ENCODE_FORMAT, self.result, self.reason)

    def from_bytes(self, data):
        (self.result,), data =  unpack_helper("?", data)
        (self.reason,), _ =  unpack_helper("10s", data)
        return self

    def __repr__(self):
        return "result: %s, reason: %s" % (self.result, self.reason)


class LogoutReq(IMessage):
    """Represent a logout request."""

    MSG_TYPE = LOGOUT_REQ
    ENCODE_FORMAT = "30s"  # nick-name

    def __init__(self, nick_name=None):
        self.nick_name = nick_name

    def to_bytes(self):
        return struct.pack(LogoutReq.ENCODE_FORMAT, self.nick_name)

    def from_bytes(self, data):
        (self.nick_name,), _ =  unpack_helper(LogoutReq.ENCODE_FORMAT, data)
        return self

    def __repr__(self):
        return "nick-name: %s" % self.nick_name


class LogoutRsp(IMessage):
    """Represent a logout response."""

    MSG_TYPE = LOGOUT_RSP
    ENCODE_FORMAT = "?10s"  # ? -> LogoutResult, 10s -> Reason

    def __init__(self, result=None, reason=None):
        self.result = result
        self.reason = reason

    def to_bytes(self):
        return struct.pack(LogoutRsp.ENCODE_FORMAT, self.result, self.reason)

    def from_bytes(self, data):
        (self.result,), data =  unpack_helper("?", data)
        (self.reason,), _ =  unpack_helper("10s", data)
        return self

    def __repr__(self):
        return "result: %s, reason: %s" % (self.result, self.reason)


class ChatMessage(IMessage):
    """Represent a single chat message."""

    MSG_TYPE = CHAT_MSG
    ENCODE_FORMAT = "30s1024s"  # 30s -> receiver's nick-name, 1024s -> chat-msg

    def __init__(self, msg_to=None, msg_content=None):
        self.msg_to = msg_to
        self.msg_content = msg_content

    def to_bytes(self):
        return struct.pack(ChatMessage.ENCODE_FORMAT, self.msg_to, self.msg_content)

    def from_bytes(self, data):
        (self.msg_to,), data = unpack_helper("30s", data)
        (self.msg_content,), _ = unpack_helper("1024s", data)
        return self

    def __repr__(self):
        return "peer: %s, msg: %s" % (self.msg_to, self.msg_content)


class BroadcastMessage(IMessage):
    """Represent a broadcast chat message."""

    MSG_TYPE = BROADCAST_MSG
    ENCODE_FORMAT = "II"  # TODO: elaborate this later

    def __init__(self, msg_from, msg_to):
        self.msg_from = msg_from
        self.msg_to = msg_to

    def to_bytes(self):
        return struct.pack(BroadcastMessage.ENCODE_FORMAT, self.msg_from, self.msg_to)
