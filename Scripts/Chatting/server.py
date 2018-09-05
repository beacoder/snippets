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

import os
import time
from socketserver import BaseRequestHandler, UDPServer


def check_db():
    """Check if db is ready.

    Check if db is ready, if not, create db and initialize
    all tables.
    """

    if not os.path.exists('./db.sqlite'):
        from sqlalchemy import create_engine
        from sqlalchemy import MetaData
        from sqlalchemy import Table
        from sqlalchemy import Column
        from sqlalchemy import Integer, String

        db_uri   = 'sqlite:///db.sqlite'
        engine   = create_engine(db_uri)
        metadata = MetaData(engine)

        users_table = Table('Users', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('ipaddr', String),
                            Column('message', String))
        metadata.create_all()

        for _t in metadata.tables:
           print("Table: ", _t)
    pass


class EchoHandler(BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        print('Got message {msg} from {peer}.'.format(msg=data,
              peer=self.client_address))
        print('Sent message {msg} to {peer}.'.format(msg=data,
              peer=self.client_address))
        print('')
        sock.sendto(data, self.client_address)


def main():
    check_db()

    with UDPServer(('', 1223), EchoHandler) as serv:
        serv.serve_forever()


if __name__ == '__main__':
    main()
