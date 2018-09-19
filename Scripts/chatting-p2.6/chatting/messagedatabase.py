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

from collections import deque


class MessageDatabase(object):
    """Store information from incomming messages."""

    def __init__(self):
        self._online_clients = {}    # client_name : ip_address
        self._online_clients_2 = {}  # ip_address : client_name
        self._offline_clients = []   # client_name
        self._offline_messages = {}  # client_name : deque(messages)

    def active_client(self, name, address):
        if not name in self._online_clients:
            self._online_clients[name] = address
            self._online_clients_2[address] = name
            if name in self._offline_clients:
                self._offline_clients.remove(name)
                # TODO: send out offline_messages for this client
            return True
        return False

    def deactive_client(self, name):
        if name in self._online_clients:
            del self._online_clients[name]
            del self._online_clients_2[address]
            if not name in self._offline_clients:
                self._offline_clients.append(name)
                return True
        return False

    def get_online_clients(self):
        return self._online_clients.keys

    def is_client_online(self, name=None, address=None):
        if name is not None:
            return name in self._online_clients
        elif address is not None:
            return address in self._online_clients_2
        else:
            return False

    def is_client_online(self, name):
        return name in self._offline_clients

    def get_client_name(self, address):
        if address in self._online_clients_2:
            return self._online_clients_2[address]
        else:
            return None

    def get_client_address(self, name):
        if name in self._online_clients:
            return self._online_clients[name]
        else:
            return None
