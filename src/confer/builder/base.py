# coding: utf-8
"""Base builder class implementation.
"""


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


class UriBasedBuilder(object):  # mix-in

    @staticmethod
    def build_init_args(parsed_uri, extra_kwargs):
        return [], dict(extra_kwargs)

    @classmethod
    def from_uri(cls, parsed_uri, extra_kwargs):
        args, kwargs = cls.build_init_args(parsed_uri, extra_kwargs or {})
        return cls(*args, **kwargs)


