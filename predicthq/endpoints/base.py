# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

import six


class MetaEndpoint(type):

    def __new__(mcs, name, bases, data):
        if 'Meta' not in data:
            class Meta:
                """ Used by decorators when overriding schema classes """
                pass
            data['Meta'] = Meta
        return super(MetaEndpoint, mcs).__new__(mcs, name, bases, data)


class BaseEndpoint(six.with_metaclass(MetaEndpoint)):

    def __init__(self, client):
        self.client = client
