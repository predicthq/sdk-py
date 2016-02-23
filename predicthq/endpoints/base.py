# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function


class BaseEndpoint(object):

    def __init__(self, client):
        self.client = client
