# -*- coding: utf-8 -*-

from dotted.collection import DottedCollection


def dot(value):
    """Converts a value into a DottedCollection"""
    return DottedCollection.factory(value)


def dot_json(json_value):
    """Creates a DottedCollection from a JSON string"""
    return DottedCollection.load_json(json_value)
