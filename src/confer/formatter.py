
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
