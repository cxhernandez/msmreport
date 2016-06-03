from time import time

import nbformat
from os.path import dirname

TEMPLATE = dirname(__file__) + '/assets/templates/template.ipynb'


class Timing(object):
    "Context manager for printing performance"

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.start = time()

    def __exit__(self, ty, val, tb):
        end = time()
        print("%s: %0.3f seconds" % (self.name, end - self.start))
        return False


def nb_template(yaml):
    with open(TEMPLATE, 'r') as f:
        nb = nbformat.read(f, nbformat.NO_CONVERT)
    for i, cell in enumerate(nb['cells']):
        nb['cells'][i]['source'] = cell['source'].format(yaml=yaml)
    return nb


def convert_keys_to_string(dictionary):
    """Recursively converts dictionary keys to strings.

    http://stackoverflow.com/questions/1254454/fastest-way-to-convert-a-dicts-keys-values-from-unicode-to-str
    """
    if isinstance(dictionary, unicode):
        return str(dictionary)
    elif not isinstance(dictionary, dict):
        return dictionary

    return (dict((str(k), convert_keys_to_string(v))
            for k, v in dictionary.items()))
