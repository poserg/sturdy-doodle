#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os

import pandas as pd
from datetime import datetime

class Company:

	def __init__(self, name):
	    self.name = name

def parse_dividends(lines, start_year, end_year, period = 'Y'):
	df = pd.DataFrame(lines, columns=['announce', 'date', 'year', 'amount'])
	df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y', errors='coerce')
	df['amount'] = df['amount'].astype(float)
	dates = pd.DataFrame(pd.date_range(datetime(start_year, 1, 1), datetime(end_year-1, 12, 31), freq = 'D'), columns=['date'])

	df.set_index('date')
	df = dates.merge(df, how='left', on='date')
	# print(df)
	df = df.groupby(df['date'].dt.to_period(period))['amount'].sum()
	df = df.round(5)
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

def aggregate_companies():
	with open('dividends_links.txt', 'r') as f:
		lines = [line.rstrip() for line in f]

	companies = []
	for l in lines:
		lst = l.split(";")
		url = lst[0]
		name = lst[1]
		table = load_dividends(url)
		if len(table) == 0:
			continue
		divs = parse_dividends(table, 2006, 2022)
		print(name, divs)
		s = 0
		for d in divs:
			s = s + d
		if s == 0:
			continue
		company = Company(name)
		company.divs = divs
		company.equities = select_equity_by_interval(get_equity(name), 2006, 2022)
		companies.append(company)
	return companies

def main():
	companies=aggregate_companies()
	for c in companies:
		s = c.name
		for i in c.equities:
			s = s + ';' + str(i)
		print (s)
	print("\n\n")
	for c in companies:
		s = c.name
		for i in c.divs:
			s = s + ';' + str(i)
		print (s)

def get_equity(name):
	dirs = os.listdir('./out/')

	filename = None
	for file in dirs:
		if name.lower() == file.lower() or name.lower() + ' ао' == file.lower():
			filename = file
			break
	if filename:
		with open('./out/' + filename, 'r') as f:
			lines = [line.rstrip() for line in f][1:]
		# end_year_cost = []
		# for l in lines:
		# 	record = l.split(';')
		# 	print (record[2][4:6])
		# 	if record[2][4:6] == '12':
		# 		end_year_cost.append([record[2], record[4]])
		# print(end_year_cost)
		return lines

def select_equity_by_interval(equities, start_year, end_year):
	# print(equities)
	result = []
	for i in range(start_year, end_year):
		date = str(i) + '1201'
		amount = 0
		for j in equities:
			record = j.split(";")
			if date == record[2]:
				amount = float(record[4])
				break
		result.append(amount)
	return result

if __name__ == "__main__":
	main()
