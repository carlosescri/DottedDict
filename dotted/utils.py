# -*- coding: utf-8 -*-

from dotted.collection import DottedCollection


def dot(value):
    return DottedCollection.factory(value)


def dot_json(json_value):
    return DottedCollection.load_json(json_value)
