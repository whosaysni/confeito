# coding: utf-8
"""Confeito: a configuration preparation library for python project.
"""
from inspect import currentframe, getmodule



class ConfigurationError(Exception):
    pass


class FormatterBase(object):
    """Base formatter implementation.

    >>> f = FormatterBase()
    >>> f.build_params()
    NotImplemented
    >>> f.format('scheme://foo/bar')
    Traceback (most recent call last):
    ...
    TypeError: format() argument after ** must be a mapping, not NotImplementedType
    """

    def build_params(self, *args, **kwargs):
        return NotImplemented

    def format(self, url, *args, **kwargs):
        params = self.build_params(*args, **kwargs)
        return url.format(**params)


class DefaultFormatter(FormatterBase):
    """Default formatter implementation.

    >>> f = DefaultFormatter()
    >>> f.build_params()
    {'login': ..., 'gid': ..., 'uid': ..., 'hostname': ...}
    >>> f.format('scheme://{hostname}/{login}')
    'scheme://.../...'
    """

    def build_params(self, *args, **kwargs):
        from socket import gethostname
        from os import getuid, getgid, getlogin
        return dict(
            hostname=gethostname(),
            uid=getuid(),
            gid=getgid(),
            login=getlogin(),
        )

default_formatter = DefaultFormatter()


class BuilderBase(object):
    """

    >>> b = BuilderBase()
    >>> b.build_configuration() == {}
    True
    >>> b.build_configuration()
    {}

    """

    def build_configuration(self):
        return {}


class SchemeBuilderBase(BuilderBase):

    def __init__(self, url, formatter=default_formatter):
        if formatter:
            url = formatter.format(url)
        from urllib2.urlparse import urlparse
        parsed = urlparse(url)
        for key in ('scheme', 'netloc', 'path', 'params', 'query', 'fragment'):
            setattr(self, key, getattr(parsed, key, ''))


class FileSchemeBuilder(SchemeBuilderBase):
    loaders = {
        # 'py': PyFileLoader,  # should be insecure
        # 'json': JsonFileLoader,
        # 'yaml': YamlFileLoader,
        # 'ini': ConfigFileLoader,
    }

    def _find_loader(self, scheme):
        self.LOADERS

    def buuld_configuration(self):
        pass  # TBA

        
class Configurator(object):

    def configure(self, *builders, **overrides):
        """Build and inject configuration."""
        module = getmodule(currentframe().f_back)
        # remove footprints
        for name, obj in module.__dict__.items():
            if obj == self.configure:
                delattr(module, name)
        # prepare settings
        config_src = {}
        # update with builders
        try:
            for builder in builders:
                if isinstance(builder, basestring):
                    builder = SchemaBuilder(builder)
                config_src.update(builder.build_configuration())
        except Exception as exc:
            raise ConfigurationError(exc)
        # update explicit settings
        config_src.update(overrides)
        # inject configuration
        for key, value in config_src.items():
            setattr(module, key, value)

            
configure = Configurator().configure


if __name__ == '__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
