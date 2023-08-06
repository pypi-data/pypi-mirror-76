import argparse
import csv
from datetime import date, datetime, timedelta
import os
import sys

# pip install tiingo first
from tiingo import TiingoClient


def main():
    parser = argparse.ArgumentParser(description="Returns the most recent \
            closing prices and trailing twelve months dividends for stocks")
    parser.add_argument('ticker_file', type=str,
            help='Ticker file name: One ticker per line',)
    parser.add_argument('--output_file', type=str,
            help='Output file name: Default writes to stdout')
    parser.add_argument('--end_date', type=str, 
            help='Date to get prices on: Default most recent closing date. \
                The date should be entered as YYYY-MM-DD \
                    trailing 12 months dividends are also relative to this date')
    parser.add_argument('--nyse_pref', action='store_true',
            help='Attempt to recognize NYSE Preferred ticker symbols and convert to tiingo friendly format. \
            Warning may produce incorrect results for non NYSE stocks with PR in their ticker name')
    parser.add_argument('--version', action='version', version='0.3.0')
    args = parser.parse_args()
    out_file = args.output_file
    end_date = args.end_date

    if end_date:
        end_date = date.fromisoformat(end_date)
    else:
        end_date = date.today()
    print("end_date = {}".format(end_date))

    if out_file:
        if os.path.isfile(out_file):
            overwrite = yes_or_no('File {} exists, do you wish to overwrite it:'.format(out_file))
            if (overwrite is False):
                print('Aborting')
                sys.exit()

    if ('TIINGO_API_KEY' not  in os.environ):
        print('Please set the TIINGO_API_KEY environment variable.')
        sys.exit(1)

    tiingo_key = os.environ['TIINGO_API_KEY']
    # print('TIINGO_API_KEY is set to {}'.format(tiingo_key))

    prices = get_prices(args.ticker_file, tiingo_key, args.nyse_pref, end_date)

    end_date_str = datetime.strftime(end_date,'%Y-%m-%d')

    hdr_str = 'Prices on or the last trading day before ' + end_date_str + '\n' + \
        'Ticker'  + ',' + 'Price' + ',' + 'Prior 12 Months Divs' + '\n'
    if out_file:
        with open(args.output_file, 'w') as fh:
            fh.write(hdr_str)
            for ticker, price, div in prices:
                fh.write(ticker + ',' + str(price) + ',' + str(div) + '\n')
    else:
        sys.stdout.write(hdr_str)
        for ticker, price, div in prices:
            sys.stdout.write(ticker + ',' + str(price) + ',' + str(div) + '\n')


def get_prices(ticker_file, tiingo_key, nyse_pref, end_date):

    """Obtains close of day prices for each ticker..
    Uses the tiingo API to retrive the price for tickers which are
    specified in the ticker_file.

    https://media.readthedocs.org/pdf/tiingo-python/latest/tiingo-python.pdf

    Args:
        ticker_file: A file with a ticker per line.
        tiingo_key: The tiingo API authentication key. End of day pricing data
        was free as of the time of writing Nov 2018.
        nyse_pref: Attempt to recognize tickers with PR in the ticker name and
        convert to tiingo friendly format for the lookup.
        end_date: Date to get prices from.
    Returns:
        A list of tupless. Each tuple consisting of:
            - Ticker a string
            - Price a float
            - Total Dividends a float rounded to 3 decimal places

    """

    prices = []
    config = {}
    config['session'] = True
    config['api_key'] = tiingo_key

    delta = timedelta(days=365)
    start_date  = end_date - delta

    client = TiingoClient(config)

    with open(ticker_file, newline = '') as t_file:
#        dialect = csv.Sniffer().sniff(csvfile.read(1024))
#        csvfile.seek(0)
#        reader = csv.reader(csvfile, dialect)
        for line in t_file:  # Each line contains a ticker
            #print(line )
            ticker = line.strip()

            if nyse_pref is True:
                if('PR') in ticker:
                    tiingo_ticker = ticker.replace(' ','')
                    tiingo_ticker = tiingo_ticker.replace('PR','-P-')
                    print("Found a Preferred Stock {} and looked up {}".format(
                        ticker,tiingo_ticker))
                else:
                    tiingo_ticker = ticker

            else:
                tiingo_ticker = ticker
            try:
#                price = client.get_ticker_price(tiingo_ticker, startDate=end_date,endDate=end_date)
                ly_hist = client.get_dataframe(tickers=tiingo_ticker,
                        frequency='daily',
                        startDate=start_date,
                        endDate=end_date)
                tot_divs = ly_hist['divCash'].sum()
                # Forced to use numerical indexing for the last row hence the cryptic -1,0
                print("Ticker = {} Price  = {:.3f} Divs = {:.2f}"
                        .format(ticker, ly_hist.iloc[-1,0], tot_divs))
                prices.append((ticker,
                    round(ly_hist.iloc[-1,0],3),
                    round(tot_divs, 3)))
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                print('tingo did not find {}'.format(ticker))
    return prices


def yes_or_no(question):
    reply = str(input(question+' (y/n): ')).lower().strip()
    if reply[0] == 'y':
        return True
    if reply[0] == 'n':
        return False
    else:
        return False


if __name__ == '__main__' :
    main()
