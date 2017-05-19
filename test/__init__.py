# coding: utf-8
"""Confaito unittests"""
from os.path import abspath, dirname, join
from sys import path
from unittest import TestLoader


# setup module path
TEST_DIR = dirname(abspath(__file__))
SRC_DIR = join(dirname(TEST_DIR), 'src')
path.insert(0, SRC_DIR)


def suite():
    loader = TestLoader()
    return loader.discover(start_dir=TEST_DIR)
