#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_tiingo_prices
----------------------------------

Tests for `tiingo_prices` module.
"""
import os
import subprocess


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
    # Could just do below. But using capsys for lols
    # assert "0.3.0" in result.stdout
    # Needed this to get the output to stdout. capsys would not see it otherwise.
    print(result.stdout)
    captured = capsys.readouterr()
    assert "0.3.0" in captured.out

def test_ticker_file_read(capsys):

    result = subprocess.run(
        ["python3",
         "-m",
         "tiingo_prices.tiingo_prices",
         "./tests/test_ticker_1.txt",
        ],
        text=True,
        #capture_output=True,
        stdout=subprocess.PIPE
    )
    print(result.stdout)
    captured = capsys.readouterr()
    assert "AAPL" in captured.out and "INTC" in captured.out

def test_specific_date_values(capsys):
    """Do we get a correct price and dividends for a ticker on a specific date"""
    result = subprocess.run(
        ["python3",
         "-m",
         "tiingo_prices.tiingo_prices",
         "--end_date",
         "2020-08-14",
         "./tests/test_ticker_2.txt",
        ],
        text=True,
        #capture_output=True,
        stdout=subprocess.PIPE
    )
    print(result.stdout)
    captured = capsys.readouterr()
    assert  "AAPL" in captured.out and "460.04" in captured.out \
            and "3.18" in captured.out
