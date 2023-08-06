#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tiingo_prices
----------------------------------

Tests for `tiingo_prices` module.
"""
import os
import subprocess
import pytest


#from tiingo_prices import tiingo_prices
#import tiingo_prices


def test_run_as_a_module():
    """Can this package be run as a python module?"""
    exit_status = os.system('python -m tiingo_prices.tiingo_prices --help')
    assert exit_status == 0

def test_version(capsys):
    """Does the version flag work?"""

    result = subprocess.run(
        ["python3",
         "-m",
         "tiingo_prices.tiingo_prices",
         "--version",
        ],
        text=True,
        capture_output=True
    )
    #Could just do below. But using capsys for lols
    #assert "0.3.0" in result.stdout
    # Needed this to get the output to stdout. capsys would not see it otherwise.
    print(result.stdout)
    captured = capsys.readouterr()
    assert "0.3.0" in captured.out
