# -*- coding: utf-8 -*-
import os

import pytest
import responses
from click.testing import CliRunner

import pypi_cli as pypi

HERE = os.path.abspath(os.path.dirname(__file__))

@pytest.yield_fixture
def mock_api():
    """A mock for the PyPI JSON API."""
    with open(os.path.join(HERE, 'response.json'), 'r') as fp:
        webargs_response = fp.read()
    # A valid package with a proper response
    responses.add(
        responses.GET,
        'https://pypi.python.org/pypi/webargs/json',
        body=webargs_response,
        content_type='application/json'
    )
    # A valid package with no releases
    with open(os.path.join(HERE, 'response_noreleases.json'), 'r') as fp:
        foo_response = fp.read()

    responses.add(
        responses.GET,
        'https://pypi.python.org/pypi/foo/json',
        body=foo_response,
        content_type='application/json'
    )

    # An invalid package name
    responses.add(
        responses.GET,
        'https://pypi.python.org/pypi/nope/json',
        status=404
    )
    responses.start()

    yield responses

    responses.stop()


@pytest.fixture
def package():
    return pypi.Package('webargs')


@pytest.fixture(scope='function')
def runner(mock_api):
    return CliRunner()
