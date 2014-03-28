======
dotted
======

A Python library that provides a method of accessing lists and dicts with a
dotted path notation. It is useful to access a deep path inside a complex
object composed of lists and dicts.

Quick & Dirty:
==============

    from dotted.collection import DottedCollection, DottedDict, DottedList

    obj = DottedCollection.factory(dict_or_list)
    obj = DottedCollection.load_json(json_value)
    obj = DottedDict(a_dict)
    obj = DottedList(a_list)

    from dotted.utils import dot, dot_json

    obj = dot(dict_or_list)
    obj = dot_json(json_value)

``DottedDict`` and ``DottedList`` have the same accessors as ``dict`` and ``list``
so you can iterate them as usual. Both type of objects support access via a
dotted path key.

Examples
========

Example #1: DottedList
----------------------

    obj = DottedList([0, 1, 2, 3, [4, 5, 6], 7, 8, [9, 10]])

All of these are true:

    obj[0]     ==  0
    obj['1']   ==  1
    obj['4.0'] ==  4
    obj['4.2'] ==  6
    obj[5]     ==  7
    obj['7.1'] == 10

If you want to append you can do:

    obj.append(12)

or:

    obj[8] = 11

but the latter only works if ``index == len(obj)``. In other case you will get a
very pretty exception.

Example #2: DottedDict
----------------------

    obj = DottedDict({'hello': {'world': {'wide': 'web'}}})

All of these are true:

    obj['hello'] == {'world': {'wide': 'web'}}
    obj['hello.world'] == {'wide': 'web'}
    obj['hello.world.wide'] == 'web'

    obj.hello == {'world': {'wide': 'web'}}
    obj.hello.world == {'wide': 'web'}
    obj.hello.world.wide == 'web'

Example #3: Both working together
---------------------------------

    obj = DottedCollection.factory({
        'hello': [{'world': {'wide': ['web', 'web', 'web']}}]
    })

You can access:

    obj['hello'][0]['world']['wide'][0]
    obj.hello[0].world.wide[0]
    obj.hello[0].world['wide'][0]
    obj.hello[0].world['wide.0']
    obj.hello['0.world'].wide[0]
    ...
    obj['hello.0.world.wide.0']

Example #4: When new values are dicts or lists
----------------------------------------------

    obj = DottedCollection.factory(some_obj)

    obj['some.path'] = {'hello': 'world'}  # will be converted to a DottedDict
    obj['another.path'] = ['hello']  # will be converted to a DottedList

Example #5: Shortcuts
---------------------

    from dotted.utils import dot, dot_json

    obj = dot({'hello': 'world'})
    obj = dot_json('{"hello": "world"}')

That's all!

## Tests

Run in the terminal from the parent directory:

    python -m dotted.test.test_collection
