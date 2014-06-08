# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from subprocess import check_output, CalledProcessError
import pytest

import pypi_cli


def test_pypi_cmd_without_args_exits_with_nonzero_code():
    with pytest.raises(CalledProcessError):
        run_cmd('pypi')


def test_pypi_cmd_version():
    assert run_cmd('pypi -v') == pypi.__version__ + '\n'
    assert run_cmd('pypi --version') == pypi.__version__ + '\n'


def test_no_division_by_zero_in_bargraph():
    assert pypi.TICK not in pypi.bargraph({'foo': 0})


def run_cmd(cmd):
    '''Run a shell command `cmd` and return its output.'''
    return check_output(cmd, shell=True).decode('utf-8')
