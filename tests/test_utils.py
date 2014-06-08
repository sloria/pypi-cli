# -*- coding: utf-8 -*-
import pypi_cli as pypi


def test_no_division_by_zero_in_bargraph():
    assert pypi.TICK not in pypi.bargraph({'foo': 0})
