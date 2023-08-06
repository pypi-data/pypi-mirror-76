"""
Generates performance reports for your stock portfolio.
"""

import csv
from collections import OrderedDict
import requests

def main():
    """
    Entrypoint into program.
    """
    import argparse

    parser = argparse.ArgumentParser(description='Generate report for a given stock portfolio.')
    parser.add_argument("Input_CSV", help='Input CSV file containing holdings information')
    parser.add_argument("Output_CSV", help='A path to output the CSV report')
    args = parser.parse_args()

    in_file = read_portfolio(args.Input_CSV)
    stocks_list = ','.join(number['symbol'] for number in in_file)
    data = get_market_data(stocks_list)
    out_file = calculate_metrics(in_file, data)
    save_portfolio(out_file, args.Output_CSV)


def read_portfolio(filename):
    """Reads and returns data from a CSV file"""
    in_file = []
    with open(filename, newline='') as infile:
        csv_reader = csv.DictReader(infile)
        for row in csv_reader:
            temp_file_in = OrderedDict()
            temp_file_in['symbol'] = row['symbol']
            temp_file_in['units'] = row['units']
            temp_file_in['cost'] = row['cost']
            in_file.append(temp_file_in)
    return in_file

def get_market_data(stocklist):
    """Gets latest price for the given stock tickers"""
    payload = {'symbols': stocklist, 'filter': 'symbol,price'}
    url = 'https://api.iextrading.com/1.0/tops/last'
    response = requests.get(url, params=payload)
    data = response.json()
    return data

def calculate_metrics(in_file, data):
    """Calculates various other metrics for the report"""
    outfile = []
    array_len = len(in_file)
    book_value = 0.0
    market_value = 0.0
    gain_loss = 0.0
    change = 0.0
    for number in range(array_len):
        temp_file_calc = OrderedDict()
        temp_file_calc = in_file[number]
        temp_file_calc.update({'price':data[number]['price']})
        book_value = round((float(in_file[number]['units'])*float(in_file[number]['cost'])), 2)
        temp_file_calc.update({'book_value':book_value})
        market_value = round((float(in_file[number]['units'])*float(data[number]['price'])), 2)
        temp_file_calc.update({'market_value':market_value})
        gain_loss = round((market_value-book_value), 2)
        temp_file_calc.update({'gain_loss':gain_loss})
        change = round((gain_loss/book_value), 4)
        temp_file_calc.update({'change':change})
        outfile.append(temp_file_calc)
        number += 1
    return outfile

def save_portfolio(csv_data, filename):
    """Saves data to a CSV file"""
    with open(filename, 'w', newline='') as outfile:
        for number in range(1):
            fnames = []
            for key in csv_data[number]:
                fnames.append(key)
        writer = csv.DictWriter(outfile, fieldnames=fnames)
        writer.writeheader()
        writer.writerows(csv_data)

if __name__ == '__main__':
    main()
