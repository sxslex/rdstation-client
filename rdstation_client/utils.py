# -*- coding: utf-8 -*-


def encode_all_unicode(obj):
    if hasattr(obj, 'encode'):
        if not isinstance(obj, str):
            return obj.encode('utf-8')
    if isinstance(obj, dict):
        new = {}
        for key in obj.keys():
            new[encode_all_unicode(key)] = encode_all_unicode(obj[key])
        return new
    if isinstance(obj, list):
        return [encode_all_unicode(item) for item in obj]
    return obj
