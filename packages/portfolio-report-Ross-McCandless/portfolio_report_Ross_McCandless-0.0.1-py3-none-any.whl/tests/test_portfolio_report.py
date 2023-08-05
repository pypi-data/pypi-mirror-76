from portfolio import portfolio_report
import pytest
import requests

def test_sourceArg_ParseArgs():
    args = portfolio_report.ParseArgs(['--source', 'portfolio.csv', '--target', 'output.csv'])
    assert args.source == 'portfolio.csv'
def test_targetArg_ParseArgs():
    args = portfolio_report.ParseArgs(['--source', 'portfolio.csv', '--target', 'output.csv'])
    assert args.target == 'output.csv'
def test_WrongParameters_ParseArgs():
    with pytest.raises(SystemExit):
        portfolio_report.ParseArgs(['--Test', 'portfolio.csv', '--haha', 'output.csv'])
def test_getCurrentMarketData(requests_mock):
    requests_mock.get(r"https://api.iextrading.com/1.0/tops/last?symbols=AMZN", text='data')
    assert 'data' == requests.get(r"https://api.iextrading.com/1.0/tops/last?symbols=AMZN").text
