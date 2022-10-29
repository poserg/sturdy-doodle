#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from calc_div import parse_dividends, load_dividends

class Company:

	def __init__(self, name):
	    self.name = name

def aggregate_companies():
	with open('./rsrc/dividends_links.txt', 'r') as f:
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
