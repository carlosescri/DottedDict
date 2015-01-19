# -*- coding: utf-8 -*-
import json

from six import string_types, text_type
import unittest2 as unittest

from dotted.collection import DottedCollection, DottedList, DottedDict


class DottedCollectionTests(unittest.TestCase):

    def assertReprsEqual(self, a_repr, b_repr):
        # Accounts for fact that ordering of dict keys may be different due to
        # hash randomization
        self.assertEqual(eval(a_repr), eval(b_repr))

    def test_dottedcollection(self):
        """ DottedCollection Tests """

        with self.assertRaisesRegexp(
                TypeError,
                "Can't instantiate abstract class DottedCollection with "
                "abstract methods __delitem__, __getitem__, __setitem__,"
                " to_python"):
            obj = DottedCollection()

        # DottedCollection.factory

        obj = DottedCollection.factory([1, 2, {'hi': 'world', '3': [4, 5, 6]}])
        self.assertReprsEqual(repr(obj),
                              "[1, 2, {'3': [4, 5, 6], 'hi': 'world'}]")
        self.assertIsInstance(obj, DottedCollection)
        self.assertIsInstance(obj, DottedList)
        self.assertIsInstance(obj[2], DottedDict)
        self.assertIsInstance(obj[2]['3'], DottedList)
        self.assertIsInstance(obj[2]['3'][0], int)
        self.assertIsInstance(obj[2]['hi'], str)

        obj = DottedCollection.factory({'hi': [1, 2, {'3': 4}], 'world': 5})
        self.assertReprsEqual(repr(obj), "{'world': 5, 'hi': [1, 2, {'3': 4}]}")
        self.assertIsInstance(obj, DottedCollection)
        self.assertIsInstance(obj, DottedDict)
        self.assertIsInstance(obj['hi'], DottedList)
        self.assertIsInstance(obj['hi'][2], DottedDict)
        self.assertIsInstance(obj['hi'][0], int)
        self.assertIsInstance(obj['world'], int)

        self.assertEqual(DottedCollection.factory(1), 1)
        self.assertEqual(DottedCollection.factory(None), None)

        # DottedCollection.load_json

        json_value = '[1, 2, {"test": [], "hello": "world"}]'
        obj = DottedCollection.load_json(json_value)
        self.assertReprsEqual(repr(obj),
                              "[1, 2, {u'test': [], u'hello': u'world'}]")
        self.assertIsInstance(obj, DottedList)
        self.assertIsInstance(obj[0], int)
        self.assertIsInstance(obj[1], int)
        self.assertIsInstance(obj[2], DottedDict)
        self.assertIsInstance(obj[2]['test'], DottedList)
        self.assertIsInstance(obj[2]['hello'], text_type)  # JSON uses unicode

        json_value = '{"test": [1, 2, {}], "hello": "world"}'
        obj = DottedCollection.load_json(json_value)
        self.assertReprsEqual(repr(obj),
                              "{u'test': [1, 2, {}], u'hello': u'world'}")
        self.assertIsInstance(obj, DottedDict)
        self.assertIsInstance(obj['test'], DottedList)
        self.assertIsInstance(obj['test'][0], int)
        self.assertIsInstance(obj['test'][1], int)
        self.assertIsInstance(obj['test'][2], DottedDict)
        self.assertIsInstance(obj['hello'], text_type)

        json_value = "Hi everybody!"
        obj = DottedCollection.load_json(json_value)
        self.assertReprsEqual(repr(obj), "'Hi everybody!'")
        self.assertIsInstance(obj, string_types)

        # DottedCollection._factory_by_index

        obj = DottedCollection._factory_by_index(1)
        self.assertIsInstance(obj, DottedList)

        obj = DottedCollection._factory_by_index('1')
        self.assertIsInstance(obj, DottedList)

        obj = DottedCollection._factory_by_index('1.1')
        self.assertIsInstance(obj, DottedList)

        obj = DottedCollection._factory_by_index('1.something')
        self.assertIsInstance(obj, DottedList)

        obj = DottedCollection._factory_by_index('1.something.1')
        self.assertIsInstance(obj, DottedList)

        obj = DottedCollection._factory_by_index('something')
        self.assertIsInstance(obj, DottedDict)

        obj = DottedCollection._factory_by_index('something.1')
        self.assertIsInstance(obj, DottedDict)

        obj = DottedCollection._factory_by_index('something.something')
        self.assertIsInstance(obj, DottedDict)

        obj = DottedCollection._factory_by_index(None)
        self.assertIsInstance(obj, DottedDict)

        # DottedCollection.to_json

        obj = DottedCollection.factory([])
        self.assertReprsEqual(obj.to_json(), '[]')

        obj = DottedCollection.factory(
            [1, 2, {'a': 'b', 'c': [3, 4, {'5': 6}]}]
        )
        self.assertReprsEqual(obj.to_json(),
                              '[1, 2, {"a": "b", "c": [3, 4, {"5": 6}]}]')

        obj = DottedCollection.factory({})
        self.assertReprsEqual(obj.to_json(), '{}')

        obj = DottedCollection.factory(
            {'a': 'b', 'c': [1, 2, {'d': [3, 4, [5]]}]}
        )
        self.assertReprsEqual(obj.to_json(),
                              '{"a": "b", "c": [1, 2, {"d": [3, 4, [5]]}]}')
        self.assertEqual(obj['c'].to_json(), '[1, 2, {"d": [3, 4, [5]]}]')
        self.assertEqual(obj['c'][2].to_json(), '{"d": [3, 4, [5]]}')
        self.assertEqual(obj['c'][2]['d'].to_json(), '[3, 4, [5]]')
        self.assertEqual(obj['c'][2]['d'][2].to_json(), '[5]')

        with self.assertRaisesRegexp(
                AttributeError,
                "'int' object has no attribute 'to_json'"):
            obj['c'][2]['d'][2][0].to_json()

    def test_dottedlist(self):
        """ DottedList Tests """
        obj = DottedList()

        self.assertNotIsInstance(obj, list)

        with self.assertRaisesRegexp(IndexError, 'list index out of range'):
            obj[0]

        self.assertReprsEqual(repr(obj), '[]')

        # If <index> == len(<DottedList>) it uses append()
        obj[0] = 0
        obj[1] = 1

        # Bad try
        with self.assertRaisesRegexp(
                IndexError,
                'list (assignment )?index out of range'):
            obj[3] = 3

        # Good!
        obj.append(2)

        self.assertReprsEqual(repr(obj), '[0, 1, 2]')

        # Bad try in nested list
        with self.assertRaisesRegexp(
                IndexError,
                'list (assignment )?index out of range'):
            obj['3.1'] = 1

        # TODO(@carlosescri): Should it be '[0, 1, 2]'???
        self.assertReprsEqual(repr(obj), '[0, 1, 2, []]')
        self.assertIsInstance(obj[3], DottedList)

        obj['3.0'] = 3
        obj['3.1'] = 4
        obj['3.2'] = [5, 6]

        self.assertReprsEqual(repr(obj), '[0, 1, 2, [3, 4, [5, 6]]]')
        self.assertIsInstance(obj['3.2'], DottedList)
        self.assertIsInstance(obj[3][2], DottedList)
        self.assertEqual(obj['3.2'], obj[3][2])

        obj['4'] = 7

        self.assertReprsEqual(repr(obj), '[0, 1, 2, [3, 4, [5, 6]], 7]')

        obj[4] = 8
        obj.insert(4, 7)

        self.assertReprsEqual(repr(obj), '[0, 1, 2, [3, 4, [5, 6]], 7, 8]')

        del obj[5]
        del obj['4']
        del obj['3.2']

        self.assertReprsEqual(repr(obj), '[0, 1, 2, [3, 4]]')

        del obj['3']

        self.assertReprsEqual(repr(obj), '[0, 1, 2]')

        obj[3] = 3

        self.assertReprsEqual(repr(obj), '[0, 1, 2, 3]')

        del obj[0]

        self.assertReprsEqual(repr(obj), '[1, 2, 3]')

        with self.assertRaisesRegexp(
                IndexError,
                'list (assignment )?index out of range'):
            del obj[3]

        python_obj = obj.to_python()

        self.assertReprsEqual(repr(python_obj), repr(obj))
        self.assertIsInstance(python_obj, list)
        self.assertNotIsInstance(obj, list)

    def test_dotteddict(self):
        """ DottedDict Tests """
        obj = DottedDict()

        self.assertNotIsInstance(obj, dict)

        with self.assertRaisesRegexp(
                KeyError,
                'DottedDict keys must be str or unicode'):
            obj[0] = 0

        with self.assertRaisesRegexp(
                KeyError,
                'DottedDict keys must be str or unicode'):
            obj[1.0] = 0

        obj['0'] = 0

        self.assertReprsEqual(repr(obj), "{'0': 0}")

        obj = DottedDict()
        obj.update({'hello': 'world'})

        self.assertReprsEqual(repr(obj), "{'hello': 'world'}")

        obj.update({'hello': {'world': {'wide': 'web'}}})

        self.assertReprsEqual(repr(obj),
                              "{'hello': {'world': {'wide': 'web'}}}")

        self.assertIsInstance(obj['hello'], DottedDict)
        self.assertIsInstance(obj['hello.world'], DottedDict)
        self.assertIsInstance(obj['hello.world.wide'], str)

        self.assertEqual(obj['hello.world'], obj['hello']['world'])
        self.assertEqual(obj['hello.world.wide'], obj['hello']['world']['wide'])

        obj['hello.world'].update({'free': 'tour'})

        self.assertReprsEqual(
            repr(obj),
            "{'hello': {'world': {'wide': 'web', 'free': 'tour'}}}"
        )

        # Access via __getattr__ and __setattr__

        self.assertEqual(obj.hello.world.wide, 'web')
        self.assertEqual(obj.hello.world.free, 'tour')

        obj.hello.world.wide = 'tour'
        obj.hello.world.free = 'web'

        self.assertEqual(obj.hello.world.wide, 'tour')
        self.assertEqual(obj.hello.world.free, 'web')

        self.assertReprsEqual(
            repr(obj),
            "{'hello': {'world': {'wide': 'tour', 'free': 'web'}}}"
        )

        obj.hello.world.wide = 'web'
        obj.hello.world.free = 'tour'

        self.assertReprsEqual(
            repr(obj),
            "{'hello': {'world': {'wide': 'web', 'free': 'tour'}}}"
        )

        del obj['hello.world.free']

        self.assertReprsEqual(repr(obj),
                              "{'hello': {'world': {'wide': 'web'}}}")

        del obj['hello']['world']['wide']

        self.assertReprsEqual(repr(obj), "{'hello': {'world': {}}}")

        obj['hello']['world.wide'] = 'web'

        self.assertReprsEqual(repr(obj),
                              "{'hello': {'world': {'wide': 'web'}}}")

        del obj['hello']['world.wide']

        self.assertReprsEqual(repr(obj), "{'hello': {'world': {}}}")

        obj['hello'] = 'goodbye'

        self.assertReprsEqual(repr(obj), "{'hello': 'goodbye'}")

        del obj.hello

        self.assertReprsEqual(repr(obj), "{}")

        obj.hello = 'goodbye'

        self.assertReprsEqual(repr(obj), "{'hello': 'goodbye'}")

        python_obj = obj.to_python()

        self.assertReprsEqual(repr(python_obj), repr(obj))
        self.assertIsInstance(python_obj, dict)
        self.assertNotIsInstance(obj, dict)

    def test_all(self):
        """ Power Tests """

        json_value = (
            '{"product": ['
            '{"label": "Categoría", "name":"categories", '
            ' "es_definition": {"terms": {"field": "categories_facet", '
            '                             "size":20}}},'
            '{"label": "Marca", "name":"brand", '
            ' "es_definition": {"terms": {"field": "brand_facet", "size":20}}},'
            '{"label": "Precio", "name":"price", '
            ' "es_definition": {"range": {"ranges": [{"from": 0}], '
            '                             "field": "price"}}},'
            '{"label": "Color", "name":"color", '
            ' "es_definition": {"terms": {"field": "color_facet", "size": 20}}}'
            ']}'
        )

        facets = DottedCollection.load_json(json_value)

        self.assertIsInstance(facets['product.0.es_definition.terms'],
                              DottedDict)
        self.assertEqual(facets['product.0.es_definition.terms.size'], 20)

        self.assertIsInstance(facets['product.2.es_definition.range.ranges'],
                              DottedList)
        self.assertEqual(facets['product.2.es_definition.range.ranges.0.from'],
                         0)

        # Some properties won't be accesible if they are Python reserved words.
        # This cannot be tested because it raises a SyntaxError
        #
        # tmp = facets.product[2].es_definition.range.ranges[0].from

        self.assertEqual(facets['product.2.es_definition.range.field'], 'price')
        self.assertEqual(facets.product[2].es_definition.range.field, 'price')

        facets['product.3.label'] = "Mi Color"
        facets['product.3.es_definition.terms.size'] = 30

        self.assertEqual(facets['product'][3]['es_definition']['terms']['size'],
                         30)
        self.assertEqual(facets.product[3].es_definition.terms.size, 30)

        json_value = (
            '{"product": {'
            ' "url": "http://www.mainada.es/feeds/doofinder/feed.xml",'
            ' "content_digest": "470550604637aac0d8ce899ade5b7ed5"'
            '}}'
        )

        feed = DottedCollection.load_json(json_value)

        self.assertIsInstance(feed['product'], DottedDict)
        self.assertIsInstance(feed.product, DottedDict)
        self.assertEqual(
            feed.product.url,
            'http://www.mainada.es/feeds/doofinder/feed.xml'
        )

        # Testing JSON correctness

        normal_object = json.loads(json_value)

        self.assertReprsEqual(feed.to_json(), json.dumps(normal_object))

        # Testing to_python() method

        python_object = feed.to_python()

        self.assertReprsEqual(repr(python_object), repr(feed))
        self.assertReprsEqual(repr(python_object), repr(normal_object))

        self.assertIsInstance(python_object, dict)
        self.assertIsInstance(python_object['product'], dict)


if __name__ == '__main__':
    unittest.main()
