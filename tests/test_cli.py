# -*- coding: utf-8 -*-
import mock
import pytest

import pypi_cli as pypi

@pytest.mark.usefixtures('mock_api')
class TestStat:

    def test_missing_package_arg(self, runner):
        result = runner.invoke(pypi.cli, ['stat'])
        assert result.exit_code > 0

    def test_with_package(self, runner):
        result = runner.invoke(pypi.cli, ['stat', 'webargs'])
        assert result.exit_code == 0
        assert 'Download statistics for webargs' in result.output

    def test_with_package_url(self, runner):
        result = runner.invoke(pypi.cli, ['stat', 'https://pypi.python.org/pypi/webargs'])
        assert result.exit_code == 0
        assert 'Download statistics for webargs' in result.output

@pytest.mark.usefixtures('mock_api')
class TestBrowse:

    def test_missing_package_arg(self, runner):
        result = runner.invoke(pypi.cli, ['browse'])
        assert result.exit_code > 0

    @mock.patch('pypi_cli.click.launch')
    def test_with_package(self, mock_launch, runner):
        result = runner.invoke(pypi.cli, ['browse', 'webargs'])
        assert result.exit_code == 0
        assert mock_launch.called is True
        mock_launch.assert_called_with('http://pypi.python.org/pypi/webargs')

@pytest.mark.usefixtures('mock_api')
class TestSearch:

    def test_missing_package_arg(self, runner):
        result = runner.invoke(pypi.cli, ['search'])
        assert result.exit_code > 0

    @mock.patch('pypi_cli.click.launch')
    def test_with_package_web(self, mock_launch, runner):
        result = runner.invoke(pypi.cli, ['search', '--web', "flask marshmallow"])
        assert result.exit_code == 0, result.output
        assert mock_launch.called is True
        mock_launch.assert_called_with('https://pypi.python.org/pypi?%3Aaction=search&term=flask%20marshmallow')

@pytest.mark.usefixtures('mock_api')
class TestInfo:

    def test_missing_package_arg(self, runner):
        result = runner.invoke(pypi.cli, ['info'])
        assert result.exit_code > 0

    def test_with_package(self, runner):
        result = runner.invoke(pypi.cli, ['info', 'webargs'])
        assert result.exit_code == 0
        assert 'webargs' in result.output

    def test_with_package_url(self, runner):
        result = runner.invoke(pypi.cli, ['info', 'https://pypi.python.org/pypi/webargs'])
        assert result.exit_code == 0

def test_version(runner):
    result = runner.invoke(pypi.cli, ['-v'])
    assert result.output == pypi.__version__ + '\n'
    result = runner.invoke(pypi.cli, ['--version'])
    assert result.output == pypi.__version__ + '\n'
