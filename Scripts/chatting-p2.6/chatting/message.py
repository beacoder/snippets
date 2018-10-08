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
from . import utils


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

    # __MSG_TYPE = INVALID_MSG  # in C++, use interface function instead, e.g: "virtual int getMessageType() = 0;"
    # __ENCODE_FORMAT = None    # use fixed-length for now, change to TLV if needed.

    def message_type(self):
        """Message type."""

        raise NotImplementedError

    def to_bytes(self):
        """Serialize to bytes."""

        raise NotImplementedError

    def from_bytes(self, data):
        """Deserialize from bytes."""

        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def sequence_number(self):
        """Sequence number of message."""

        raise NotImplementedError


class HeartbeatReq(IMessage):
    """Represent a heartbeat request."""

    __MSG_TYPE = HEARTBEAT_REQ
    __ENCODE_FORMAT = "15s"  # 15s -> "HeartbeatReq"

    def __init__(self):
        self._msg = "HeartbeatReq"

    def message_type(self):
        return HeartbeatReq.__MSG_TYPE

    def to_bytes(self):
        return struct.pack(HeartbeatReq.__ENCODE_FORMAT, utils.to_bytes(self._msg))

    def from_bytes(self, data):
        (data,), _ = unpack_helper(HeartbeatReq.__ENCODE_FORMAT, data)
        self._msg = utils.to_str(data)
        return self

    def __repr__(self):
        return self._msg


class HeartbeatRsp(IMessage):
    """Represent a heartbeat response."""

    __MSG_TYPE = HEARTBEAT_RSP
    __ENCODE_FORMAT = "15s"  # 15s -> "HeartbeatRsp"

    def __init__(self):
        self._msg = "HeartbeatRsp"

    def message_type(self):
        return HeartbeatRsp.__MSG_TYPE

    def to_bytes(self):
        return struct.pack(HeartbeatRsp.__ENCODE_FORMAT, utils.to_bytes(self._msg))

    def from_bytes(self, data):
        (data,), _ = unpack_helper(HeartbeatRsp.__ENCODE_FORMAT, data)
        self._msg = utils.to_str(data)
        return self

    def __repr__(self):
        return self._msg


class LoginReq(IMessage):
    """Represent a login request."""

    __MSG_TYPE = LOGIN_REQ
    __ENCODE_FORMAT = "30s"  # nick-name

    def __init__(self, nick_name=None):
        self.nick_name = nick_name

    def message_type(self):
        return LoginReq.__MSG_TYPE

    def to_bytes(self):
        return struct.pack(LoginReq.__ENCODE_FORMAT, utils.to_bytes(self.nick_name))

    def from_bytes(self, data):
        (data,), _ = unpack_helper(LoginReq.__ENCODE_FORMAT, data)
        self.nick_name = utils.to_str(data)
        return self

    def __repr__(self):
        return "nick-name: %s" % self.nick_name


class LoginRsp(IMessage):
    """Represent a login response."""

    __MSG_TYPE = LOGIN_RSP
    __ENCODE_FORMAT = "?10s"  # ? -> LoginResult, 10s -> Reason

    def __init__(self, result=None, reason=None):
        self.result = result
        self.reason = reason

    def message_type(self):
        return LoginRsp.__MSG_TYPE

    def to_bytes(self):
        return struct.pack(LoginRsp.__ENCODE_FORMAT, utils.to_bytes(self.result), utils.to_bytes(self.reason))

    def from_bytes(self, data):
        (self.result,), data = unpack_helper("?", data)
        (data,), _ = unpack_helper("10s", data)
        self.reason = utils.to_str(data)
        return self

    def __repr__(self):
        return "result: %s, reason: %s" % (self.result, self.reason)


class LogoutReq(IMessage):
    """Represent a logout request."""

    __MSG_TYPE = LOGOUT_REQ
    __ENCODE_FORMAT = "30s"  # nick-name

    def __init__(self, nick_name=None):
        self.nick_name = nick_name

    def message_type(self):
        return LogoutReq.__MSG_TYPE

    def to_bytes(self):
        return struct.pack(LogoutReq.__ENCODE_FORMAT, utils.to_bytes(self.nick_name))

    def from_bytes(self, data):
        (data,), _ = unpack_helper(LogoutReq.__ENCODE_FORMAT, data)
        self.nick_name = utils.to_str(data)
        return self

    def __repr__(self):
        return "nick-name: %s" % self.nick_name


class LogoutRsp(IMessage):
    """Represent a logout response."""

    __MSG_TYPE = LOGOUT_RSP
    __ENCODE_FORMAT = "?10s"  # ? -> LogoutResult, 10s -> Reason

    def __init__(self, result=None, reason=None):
        self.result = result
        self.reason = reason

    def message_type(self):
        return LogoutRsp.__MSG_TYPE

    def to_bytes(self):
        return struct.pack(LogoutRsp.__ENCODE_FORMAT, utils.to_bytes(self.result), utils.to_bytes(self.reason))

    def from_bytes(self, data):
        (self.result,), data = unpack_helper("?", data)
        (data,), _ = unpack_helper("10s", data)
        self.reason = utils.to_str(data)
        return self

    def __repr__(self):
        return "result: %s, reason: %s" % (self.result, self.reason)


class ChatMessage(IMessage):
    """Represent a single chat message."""

    __MSG_TYPE = CHAT_MSG
    __ENCODE_FORMAT = "30s1024s"  # 30s -> receiver's nick-name, 1024s -> chat-msg

    def __init__(self, msg_to=None, msg_content=None):
        self.msg_to = msg_to
        self.msg_content = msg_content

    def message_type(self):
        return ChatMessage.__MSG_TYPE

    def to_bytes(self):
        return struct.pack(ChatMessage.__ENCODE_FORMAT, utils.to_bytes(self.msg_to), utils.to_bytes(self.msg_content))

    def from_bytes(self, data):
        (self.msg_to,), data = unpack_helper("30s", data)
        self.msg_to = utils.to_str(self.msg_to)
        (self.msg_content,), _ = unpack_helper("1024s", data)
        self.msg_content = utils.to_str(self.msg_content)
        return self

    def __repr__(self):
        return "peer: %s, msg: %s" % (self.msg_to, self.msg_content)


class BroadcastMessage(IMessage):
    """Represent a broadcast chat message."""

    __MSG_TYPE = BROADCAST_MSG
    __ENCODE_FORMAT = "II"  # TODO: elaborate this later

    def __init__(self, msg_from, msg_to):
        self.msg_from = msg_from
        self.msg_to = msg_to

    def to_bytes(self):
        return struct.pack(BroadcastMessage.__ENCODE_FORMAT, utils.to_bytes(self.msg_to), utils.to_bytes(self.msg_content))
