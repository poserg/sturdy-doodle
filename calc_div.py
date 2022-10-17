#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

def parse_dividends(file_name):
	with open('/tmp/div.txt', 'r') as f:
		lines = [line.rstrip() for line in f]

	r = {}
	for i in xrange(2006, 2022):
		r[i] = 0

	for l in lines:
		record = l.split()
		key=int(record[1][-4:])
		if key in r:
			value=float(record[3])
			# print(value)
			r[key]=r[key]+value
	s=''
	for i in sorted(r.keys()):
	    s=s + str(r[i]) + '\t'

	print (s)

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
	print(table)