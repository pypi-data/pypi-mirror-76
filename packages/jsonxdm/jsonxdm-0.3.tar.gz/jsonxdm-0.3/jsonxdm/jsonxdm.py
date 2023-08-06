
from lxml.etree import Element 
import json

def loads(s):
    d = json.loads(s)
    return _dict_to_xdm(d)

def load(fp):
    d = json.load(fp)
    return _dict_to_xdm(d)

def dumps(xdm, indent=None, separators=None, sort_keys=False):
    d = _xdm_to_dict(xdm)
    return json.dumps(d, indent=indent, separators=separators, sort_keys=sort_keys)

def dump(xdm, fp):
    d = _xdm_to_dict(xdm)
    return json.dump(d, fp)

def _dict_to_xdm(value, key=None):
    if value is None:
        return_value = _element('null')
    elif type(value) is dict:
        return_value = _element('map')
        for (i, j) in value.items():
            return_value.append(_dict_to_xdm(j, i))
    elif type(value) is bool:
        return_value = _element('boolean')
        if value is True:
            return_value.text = 'true'
        elif value is False:
            return_value.text = 'false'
    elif type(value) is list:
        return_value = _element('array')
        for i in value:
            return_value.append(_dict_to_xdm(i))
    elif type(value) is int:
        return_value = _element('number')
        return_value.text = str(value)
    elif type(value) is str:
        return_value = _element('string')
        return_value.text = value
    if key is not None:
        return_value.set('key', key)
    return return_value

_NSMAP = {None: 'http://www.w3.org/2005/xpath-functions'}

def _element(e):
    return Element(_element_name(e), nsmap=_NSMAP)

def _element_name(e):
    return u'{http://www.w3.org/2005/xpath-functions}' + e

def _xdm_to_dict(el, context=None):
    v = None
    if el.tag == _element_name('map'):
        v = {}
        for i in el:
            _xdm_to_dict(i, v)
    elif el.tag == _element_name('array'):
        v = []
        for i in el:
            _xdm_to_dict(i, v)
    elif el.tag == _element_name('boolean'):
        v = json.loads(el.text.lower())
    elif el.tag == _element_name('number'):
        v = json.loads(el.text)
    elif el.tag == _element_name('string'):
        v = el.text
    elif el.tag == _element_name('null'):
        v = None
    if 'key' in el.attrib and type(context) is dict:
        context[el.get('key')] = v
    elif type(context) is list:
        context.append(v)
    elif context is None:
        return v

