"""
Tests I/O disk operations.
"""

from collections import OrderedDict
import requests
from portfolio import portfolio_report


# Note: the portfolio_csv argument found in the tests below
#       is a pytest "fixture". It is defined in conftest.py

# DO NOT edit the provided tests. Make them pass.

def test_read_portfolio(portfolio_csv):
    """
    Given that the read_portfolio is called, assert that
    the data the expected data is returned.
    """
    expected = [
        OrderedDict([
            ('symbol', 'APPL'),
            ('units', '100'),
            ('cost', '154.23'),
        ]),
        OrderedDict([
            ('symbol', 'AMZN'),
            ('units', '600'),
            ('cost', '1223.43')
        ])
    ]

    assert portfolio_report.read_portfolio(portfolio_csv) == expected, (
        'Expecting to get the data stored in the portfolio_csv '
        'fixture as a Python data structure.'
    )


def test_save_portfolio(portfolio_csv):
    """
    Given that the save portfolio method is called with the following
    data, assert that a CSV file is written in the expected format.

    The portfolio
    """
    data = [{'symbol': 'MSFT', 'units': 10, 'cost': 99.66}]
    portfolio_report.save_portfolio(data, filename=portfolio_csv)

    expected = 'symbol,units,cost\r\nMSFT,10,99.66\r\n'
    with open(portfolio_csv, 'r', newline='') as file:
        result = file.read()
        assert result == expected, (
            f'Expecting the file to contain: \n{result}'
        )

def test_url(requests_mock):
    """
    This will replace the the data by getting a mock value
    """
    requests_mock.get('https://api.iextrading.com/1.0/tops/last', text='data')
    assert requests.get('https://api.iextrading.com/1.0/tops/last').text == 'data'
