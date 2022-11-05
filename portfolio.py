#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clients.mfd import MfdClient
import configparser
import argparse
import logging

config_file = 'config.ini'


def main(tickers):
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
    main(tickers)
