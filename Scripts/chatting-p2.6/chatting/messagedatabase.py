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

    # TODO: save clients information in this class.

    def __init__(self):
        self._active_clients = {}    # client_name : ip_address
        self._offline_clients = []   # client_name
        self._offline_messages = {}  # client_name : deque(messages)

    def online_client(self, client_info):
        client_name = client_info['name']
        client_addr = client_info['address']
        if not client_name in self._active_clients:
            self._active_clients[client_name] = client_addr
            if client_name in self._offline_clients:
                self._offline_clients.remove(client_name)
                # TODO: send out offline_messages for this client
            return True
        return False

    def offline_client(self, client_name):
        if client_name in self._active_clients:
            del self._active_clients[client_name]
            if not client_name in self._offline_clients:
                self._offline_clients.append(client_name)
                return True
        return False

    def get_all_clients(self):
        """Return all clients, don't modify it."""

        return client_info
