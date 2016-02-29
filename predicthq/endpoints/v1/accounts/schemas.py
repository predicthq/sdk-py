# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import, print_function

from predicthq.endpoints.schemas import Model, StringType, DateTimeType


class Account(Model):

    id = StringType()
    name = StringType()
    description = StringType()
    created_at = DateTimeType()
    updated_at = DateTimeType()
