#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

import requests
from bs4 import BeautifulSoup

import pandas as pd
from datetime import datetime


def parse_dividends(lines, start_year, end_year, period='Y'):
    df = pd.DataFrame(lines, columns=['announce', 'date', 'year', 'amount'])
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y', errors='coerce')
    df['amount'] = df['amount'].astype(float)
    dates = pd.DataFrame(pd.date_range(
        datetime(start_year, 1, 1),
        datetime(end_year-1, 12, 31), freq='D'), columns=['date'])

    df.set_index('date')
    df = dates.merge(df, how='left', on='date')
    # print(df)
    df = df.groupby(df['date'].dt.to_period(period))['amount'].sum()
    df = df.round(6)
    return df.values.tolist()


def load_dividends(url):
    response = requests.get(url)
    soap = BeautifulSoup(response.text, 'lxml')
    divs = soap.findChildren('table')

    result = []
    # print(divs)
    if len(divs) < 3:
        # print("skip " + url)
        return result
    table = divs[2]
    for row in table.findChildren(['th', 'tr']):
        cells = row.findChildren('td')
        line = []
        result.append(line)
        for cell in cells:
            line.append(cell.text.strip())
    return result


def main(url, start_year, end_year, period):
    table = load_dividends(url)
    result = parse_dividends(table, start_year, end_year, period)
    print(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='url')
    parser.add_argument('-sy', type=int, dest='start_year', default=2006)
    parser.add_argument('-ey', type=int, dest='end_year', default=2022)
    parser.add_argument('-p', dest='period', default='Y', choices=['Q', 'Y'])
    args = parser.parse_args()
    main(args.url, args.start_year, args.end_year, args.period)
