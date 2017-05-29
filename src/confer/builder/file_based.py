# coding: utf-8
from __future__ import unicode_literals
from os import devnull
from os.path import abspath, normpath
from imp import load_source
from confer.builder.base import BuilderBase, UriBasedBuilder


def module_from_stream(stream):
    modname = '__confer_tmp__'
    try:
        mod = load_source(modname, devnull, stream)
    except Exception as exc:
        raise ImportError('Unable to load module from {}.'.format(repr(stream)))
    return mod
    


class FileBuilder(BuilderBase, UriBasedBuilder):

    @staticmethod
    def build_init_args(parsed_uri, extra_kwargs):
        path = normpath(abspath(parsed_uri.path))
        args = [path]
        kwargs = dict(extra_kwargs)
        return args, kwargs

    def __init__(self, path, file_format='python', **kwargs):
        self._path = path
        self._format = file_format

    def build_configuration(self):
        mod = module_from_stream(open(self._path, 'r'))
        config_dict = dict(
            (attr_name, getattr(mod, attr_name))
            for attr_name in getattr(
                mod, '__all__',
                filter(lambda k: not k.startswith('__'), dir(mod))))
        return config_dict
