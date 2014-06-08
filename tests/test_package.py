# -*- coding: utf-8 -*-
import os

import responses
import pytest

import piptool

HERE = os.path.abspath(os.path.dirname(__file__))

def setup_module():
    with open(os.path.join(HERE, 'response.json'), 'r') as fp:
        response_body = fp.read()
    responses.add(
        responses.GET,
        'http://pypi.python.org/pypi/webargs/json',
        body=response_body,
        content_type='application/json'
    )
    responses.add(
        responses.GET,
        'http://pypi.python.org/pypi/nope/json',
        status=404
    )
    responses.start()

def teardown_module():
    responses.stop()

@pytest.fixture
def package():
    return piptool.Package('webargs')

class TestPackage:

    def test_repr(self, package):
        assert repr(package) == '<Package(name={0!r})>'.format('webargs')

    def test_versions(self, package):
        vers  = ['0.1.0', '0.2.0', '0.3.0', '0.3.1',
                 '0.3.2', '0.3.3', '0.3.4', '0.4.0']
        assert package.versions == vers

    def test_downloads(self, package):
        assert package.downloads == sum(package.version_downloads.values())

    def test_max_version(self, package):
        assert package.max_version == max(package.version_downloads.items(),
                                            key=lambda item: item[1])

    def test_min_version(self, package):
        assert package.min_version == min(package.version_downloads.items(),
                                            key=lambda item: item[1])

    def test_avg_downloads(self, package):
        avg = package.downloads / len(package.versions)
        assert package.average_downloads == int(avg)
