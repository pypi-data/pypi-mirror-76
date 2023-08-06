# -*- coding: utf-8 -*-

from zc.buildout.testing import buildoutSetUp
from zc.buildout.testing import buildoutTearDown
from zc.buildout.testing import install
from zc.buildout.testing import install_develop

import doctest
import pkg_resources
import shutil
import six
import unittest


def setUp(test):
    buildoutSetUp(test)
    install_develop('plone.recipe.zope2instance', test)
    install('zc.recipe.egg', test)
    install_dependencies(pkg_resources.working_set.require('ZEO'), test)
    install_dependencies(pkg_resources.working_set.require('Zope'), test)
    install_dependencies(pkg_resources.working_set.require('ZODB'), test)


def install_dependencies(dependencies, test):
    for dep in dependencies:
        try:
            install(dep.project_name, test)
        except OSError:
            # Some distributions are installed multiple times, and the
            # underlying API doesn't check for it
            pass


def tearDown(test):
    buildoutTearDown(test)
    sample_buildout = test.globs['sample_buildout']
    shutil.rmtree(sample_buildout, ignore_errors=True)


def test_suite():
    suite = []
    flags = (
        doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE |
        doctest.REPORT_NDIFF)

    suite.append(doctest.DocFileSuite(
        'zope2instance.txt',
        'wsgi.txt',
        optionflags=flags,
        setUp=setUp,
        tearDown=tearDown))

    if six.PY2:
        suite.append(doctest.DocFileSuite(
            'zope2instance_zserver.txt',
            optionflags=flags,
            setUp=setUp,
            tearDown=tearDown))

    return unittest.TestSuite(suite)
