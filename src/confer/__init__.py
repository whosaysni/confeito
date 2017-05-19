# coding: utf-8
"""Confer: a configuration preparation library for python project.
"""
from inspect import currentframe, getmodule
from confer.builder.utils import UriLoader
from confer.exception import ConfigurationError


class Configurator(object):
    """Default configurator implementation."""

    def __init__(self, uri_loader=UriLoader(), ignore_errors=False):
        """Create a new configurator instance."""
        self._uri_loader = uri_loader
        self._ignore_errors = ignore_errors
        
    def load_settings(self, *builders, **overrides):
        """Build settings and return as a dictionary."""
        # prepare settings
        settings = {}
        # 'build' builders
        _builders = []
        for builder in builders:
            if isinstance(builder, basestring):
                _builders.append(self._uri_loader.load(builder))
            else:
                _builders.append(builder)
        # update settings with builders
        for builder in _builders:
            try:
                settings.update(builder.build_configuration())
            except Exception as exc:
                if self._ignore_errors:
                    pass
                raise ConfigurationError(exc)
        # update explicit settings
        settings.update(overrides)
        return settings

    def configure(self, *builders, **overrides):
        """Inject settings into configuration."""
        # this method should be called directly from a configuration file.
        caller_module = getmodule(currentframe().f_back)
        # remove footprints
        for name, obj in caller_module.__dict__.items():
            # exclude this module and all confer-based objects
            src_module = getmodule(obj)
            if src_module and src_module.__name__.startswith('confer'):
                delattr(src_module, name)
        # inject settings
        settings = self.load_settings(*builders, **overrides)
        for key, value in settings.items():
            setattr(caller_module, key, value)

            
configure = Configurator().configure


if __name__ == '__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
