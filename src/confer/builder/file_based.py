# coding: utf-8
from os.path import abspath, normpath
from imp import load_source
from confer.builder.base import BuilderBase, UriBasedBuilder


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
        modname = '__confer_tmp__'
        try:
            mod = load_source(modname, modname, open(self._path, 'r'))
        except Exception as exc:
            print self._path
            print vars(exc)
            raise
        return dict(
            (name, getattr(mod, name))
            for name in getattr(mod, '__all__',
                                filter(lambda k: not k.startswith('__'), dir(mod))))
            
        

        
    
