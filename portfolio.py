#!/usr/bin/env python
# -*- coding: utf-8 -*-

from portfolio.clients.mfd import MfdClient
from portfolio.clients.smart_lab import SmartLabClient
import configparser
import argparse
import logging

config_file = 'config.ini'


def main(tickers, bond):
    get_stock_prices(tickers)
    get_bond_prices([bond])


def get_bond_prices(bonds):
    smart_lab = SmartLabClient()
    for i in bonds:
        bond = smart_lab.retrieve_bond_info(i)
        print(str(bond.price).replace('.', ','))
        print(str(bond.oid).replace('.', ','))


def get_stock_prices(tickers):
    mfd = MfdClient()
    for i in tickers:
        date, price = mfd.get_last_quote(i)
        print(str(price).replace('.', ','))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c',
                        help='Config file (default \'%s\')' % config_file,
                        default=config_file,
                        dest='config',
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
    logging.basicConfig(level=args.log_level or logging.INFO)
    cfg = configparser.ConfigParser()
    cfg.read_file(open(args.config))
    tickers = cfg['portfolio']['tickers'].split(',')
    bond = cfg['portfolio']['bond']
    main(tickers, bond)
