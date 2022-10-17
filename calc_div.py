#!/usr/bin/env python
# -*- coding: utf-8 -*-

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