# coding: utf-8
"""Confer root module tests
"""
import unittest as ut

# from confer import ConfigurationError
from confer import Configurator
# from confer import configure
from confer.builder import FileBuilder
from confer.builder.utils import UriLoader
from confer.exception import ConfigurationError


class TestFileBuilder(ut.TestCase):

    def test_init(self):
        from os.path import abspath, dirname, join
        from urlparse import urlparse
        modpath = join(dirname(abspath(__file__)), 'settings/file_sample.py')
        uri = 'file://{}'.format(modpath)
        parsed_uri = urlparse(uri)
        fb = FileBuilder.from_uri(parsed_uri, None)
        self.assertEqual(fb._path, modpath)
        self.assertEqual(fb.build_configuration(), dict(COLOR='Blue', NUMBER=42))


class TestUriLoader(ut.TestCase):

    def test_init(self):
        ul = UriLoader()
        self.assertFalse(hasattr(ul, '_builder_map'))
        ul.builder_map  # noqa
        self.assertTrue(hasattr(ul, '_builder_map'))
        self.assertIsNotNone(ul._builder_map)
        self.assertIn('file', ul.builder_map)

    def test_load(self):
        ul = UriLoader()
        with self.assertRaises(ConfigurationError) as exc:
            ul.load('_nonexistent_:///foo/bar/baz')
            self.assertEqual(exc.value, {})
        b = ul.load('file:///foo/bar/baz')
        self.assertIsInstance(b, FileBuilder)


class TestConfigurator(ut.TestCase):

    def test_init(self):
        c = Configurator()
        self.assertIsInstance(c._uri_loader, UriLoader)
        self.assertFalse(c._ignore_errors)

    def test_init_param_uri_loader(self):
        c = Configurator(uri_loader=None)
        self.assertEqual(c._uri_loader, None)
                       
    def test_init_param_ignore_errors(self):
        c = Configurator(ignore_errors=True)
        self.assertTrue(c._ignore_errors)
        c = Configurator(ignore_errors=False)
        self.assertFalse(c._ignore_errors)

    def test_load_settings(self):
        c = Configurator()
        s = c.load_settings()
        self.assertEqual(s, {})
        s = c.load_settings(foo='bar')
        self.assertEqual(s, dict(foo='bar'))
        
    def test_configure(self):
        config = __import__('settings.s001').s001
        print dir(config)
        self.assertEqual(getattr(config, 'foo'), 'bar')
        self.assertFalse(hasattr(config, 'configurator'))
