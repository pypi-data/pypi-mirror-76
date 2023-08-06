# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

import collections

Serializer = collections.namedtuple('Serializer', ('objects','object_lists','values','objects_2d','custom'))

def _save_object_id_list(result, key, alist):
    if not alist:
        result[key] = []
    else:
        result[key] = [ x.obj_id for x in alist ]

def _save_object_lists(obj, result, names):
    for k in names:
        v = getattr(obj, k)
        _save_object_id_list(result, k, v)

def _save_objects(obj, result, names):
    for k in names:
        v = getattr(obj, k)
        if v:
            result[k] = v.obj_id
        else:
            result[k] = None

def _save_values(obj, result, names):
    for k in names:
        v = getattr(obj, k)
        result[k] = v

def _save_objects_2d(obj, result, names):
    for k in names:
        v = getattr(obj, k)
        if not v:
            result[k] = []
            return
        detail = []
        for x in v:
            if type(x) == list:
                detail.append([x.obj_id for i in x])
            else:
                detail.append(x.obj_id)
        result[k] = detail

def _save_custom(obj, result, custom):
    for x in custom:
        value = getattr(obj, "load_%s" % x)()
        result[x] = value

def _save(obj, object_lists=None, objects=None, values=None, objects_2d=None, custom=None):
    results = dict(obj_id=obj.obj_id)
    _save_object_lists(obj, results, object_lists)
    _save_objects(obj, results, objects)
    _save_values(obj, results, values)
    _save_objects_2d(obj, results, objects_2d)
    _save_custom(obj, results, custom)
    return results

def save_object(obj):

    return _save(obj,
        object_lists=obj.__class__.SERIALIZER.object_lists,
        objects=obj.__class__.SERIALIZER.objects,
        values=obj.__class__.SERIALIZER.values,
        objects_2d=obj.__class__.SERIALIZER.objects_2d,
        custom=obj.__class__.SERIALIZER.custom,
    )

def _get_finder(song, key):
    if key.endswith("s"):
        return getattr(song, "find_%s" % key[:-1])
    else:
        return getattr(song, "find_%s" % key)

def _load(cls, song, data, object_lists=None, objects=None, values=None, objects_2d=None, custom=None):


    kwargs = {}
    kwargs["obj_id"] = data["obj_id"]

    for k in values:
        kwargs[k] = data[k]

    for k in objects:
        finder = _get_finder(song, k)
        kwargs[k] = finder(data[k])

    for k in object_lists:
        finder = _get_finder(song, k)
        kwargs[k] = [ finder(x) for x in data[k] ]

    for k in objects_2d:
        detail = []
        finder = _get_finder(song, k)
        data_item = data[k]
        for x in data_item:
            if type(x) == list:
                detail.append([ finder(i) for i in x ])
            else:
                detail.append( finder(x) )
        kwargs[k] = detail

    obj = cls(**kwargs)

    for k in custom:
        method = getattr(obj, "load_%s" % k)
        value = method(song, data[k])
        setattr(obj, k, value)

    return obj


def load_object(cls, song, data):
    return _load(cls, song, data,
        object_lists=cls.SERIALIZER.object_lists,
        objects=cls.SERIALIZER.objects,
        values=cls.SERIALIZER.values,
        objects_2d=cls.SERIALIZER.objects_2d,
        custom=cls.SERIALIZER.custom
    )