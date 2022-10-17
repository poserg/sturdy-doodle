#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

def parse_dividends(lines):
	r = {}
	for i in range(2006, 2022):
		r[i] = 0

	for l in lines:
		# print(l)
		if len(l) < 4 or len(l[1]) != 10:
			continue
		key=int(l[1][-4:])
		if key in r:
			value=float(l[3])
			# print(value)
			r[key]=r[key]+value

	result = []
	for i in sorted(r.keys()):
	    result.append(r[i])

	return result

def load_dividends(url):
	response = requests.get(url)
	soap = BeautifulSoup(response.text, 'lxml')
	divs = soap.findChildren('table')

	table = divs[2]
	result = []
	for row in table.findChildren(['th', 'tr']):
		cells = row.findChildren('td')
		line = []
		result.append(line)
		for cell in cells:
			line.append(cell.text.strip())
	return result

if __name__ == "__main__":
	table = load_dividends('https://www.dohod.ru/ik/analytics/dividend/agro')
	divs = parse_dividends(table)
	print(divs)