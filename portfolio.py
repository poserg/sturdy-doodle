#!/usr/bin/env python
# -*- coding: utf-8 -*-

from portfolio.clients.mfd import MfdClient
from portfolio.clients.smart_lab import SmartLabClient
import configparser
import argparse
import logging

config_file = 'config.ini'
year = None


def main(tickers, bond):
    get_stock_prices(tickers)
    get_bond_prices([bond])


def get_bond_prices(bonds):
    smart_lab = SmartLabClient()
    for i in bonds:
        bond = smart_lab.retrieve_bond_info(i)
        print(_num_to_str, bond.price)
        print(_num_to_str, bond.oid)


def _num_to_str(string):
    return str(string).replace('.', ',')


def get_stock_prices(tickers):
    mfd = MfdClient()
    for i in tickers:
        if year:
            stocks = mfd.get_by_year(
                i,
                '01.01.' + str(year),
                '01.12.' + str((year+1)))
            for s in stocks:
                print(f"{s.name};+{_num_to_str(s.price)}")
        else:
            stock = mfd.get_last_quote(i)
            print(map(_num_to_str, stock.price))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        help='Config file (default \'%s\')' % config_file,
                        default=config_file,
                        dest='config',
                        )
    parser.add_argument('-y',
                        help='Year (default: None)',
                        default=None,
                        dest='year',
                        type=int,
                        )
    parser.add_argument('-v',
                        '--verbose',
                        help='Verbose (debug) logging',
                        action='store_const',
                        const=logging.DEBUG,
                        dest='log_level')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    year = args.year
    logging.basicConfig(level=args.log_level or logging.INFO)
    cfg = configparser.ConfigParser()
    cfg.read_file(open(args.config))
    tickers = cfg['portfolio']['tickers'].split(',')
    bond = cfg['portfolio']['bond']
    main(tickers, bond)
