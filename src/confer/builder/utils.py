# coding: utf-8
"""Builder loaders.
"""
from urlparse import urlparse
from confer.exception import ConfigurationError
from confer.builder.file_based import FileBuilder


class BuilderLoaderBase(object):

    def load(self, *args, **kwargs):
        return NotImplemented


class UriLoader(BuilderLoaderBase):
    DEFAULT_BUILDERS_MAP = (
        ('file', (FileBuilder, None)),
        # ('http', (HttpBuilder, None)),
        # ('https', (HttpBuilder, None)),
        # ('ssh', (SshBuilder, None)),
        # ('git', (GitBuilder, None)),
        # ('git+ssh', (GitBuilder, None)),
        # ('git+https', (GitBuilder, None)),
        # ('s3', (S3Builder, None)),
    )

    @property
    def builder_map(self):
        if not hasattr(self, '_builder_map'):
            self._builder_map = dict(self.DEFAULT_BUILDERS_MAP)
        return self._builder_map

    def load(self, uri):
        parsed_uri = urlparse(uri)
        found = self.builder_map.get(parsed_uri.scheme, None)
        if found is None:
            raise ConfigurationError(
                'Builder does not exist.',
                dict(scheme=parsed_uri.scheme))
        builder_cls, extra_kwargs = found
        return builder_cls.from_uri(parsed_uri, extra_kwargs)
