# -*- coding: utf-8 -*-
import pytest

import pypi_cli as pypi


@pytest.mark.usefixtures('mock_api')
class TestPackage:

    def test_repr(self, package):
        assert repr(package) == '<Package(name={0!r})>'.format('webargs')

    def test_versions(self, package):
        vers = ['0.1.0', '0.2.0', '0.3.0', '0.3.1',
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

    def test_package_not_found(self):
        package = pypi.Package('nope')
        with pytest.raises(pypi.NotFoundError):
            package.data

    def test_package_with_no_releases(self):
        package = pypi.Package('foo')
        assert package.downloads == 0
        assert package.min_version == (None, 0)
