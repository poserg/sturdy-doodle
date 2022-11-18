import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class Bond:

    def __init__(self, price, oid):
        self._price = price
        self._oid = oid  # Original Issue Discount

    @property
    def price(self):
        return self._price

    @property
    def oid(self):
        return self._oid


class SmartLabClient:

    def __init__(self):
        self.url = 'https://smart-lab.ru/q/bonds/'

    def retrieve_bond_info(self, ticker):
        bond_table = self._get_bond_table(self.url + ticker)
        price = None
        oid = None
        for row in bond_table.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) > 1:
                if columns[0].abbr.text == 'Цена послед':
                    price = float(columns[1].text)
                if columns[0].abbr['title'] == 'Накопленный купонный доход':
                    oid = columns[1].text
                if price is not None and oid is not None:
                    return Bond(price, float(oid.split(' ')[0]))

    def _get_bond_table(self, url):
        response = requests.get(url)
        soap = BeautifulSoup(response.text, 'html.parser')
        bond_table = soap.find_all('table')
        return bond_table[0]
