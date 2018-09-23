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

import logging


VERBOSE_LEVEL = 5

verbose = 0


def prepare_logger(logfile):
    global verbose

    logging.basicConfig(filename=logfile,
                        level=logging.INFO,
                        format="%(asctime)s %(levelname)s - %(message)s")
    logging.getLogger('').handlers = []
    logging.addLevelName(VERBOSE_LEVEL, 'VERBOSE')

    config = {'verbose':0}
    if config['verbose'] >= 2:
        level = VERBOSE_LEVEL
    elif config['verbose'] == 1:
        level = logging.DEBUG
    elif config['verbose'] == -1:
        level = logging.WARN
    elif config['verbose'] <= -2:
        level = logging.ERROR
    else:
        level = logging.INFO
    verbose = config['verbose']

    logging.basicConfig(level=level,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logging.info("log starts here")


# from ssloop
def print_exception(e):
    global verbose
    logging.error(e)
    if verbose > 0:
        import traceback
        traceback.print_exc()
