#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import base64
import zlib

d = {}

for line in sys.stdin:
	num, text = line.rstrip('\n').split('\t')
	num = int(num) + 1
	words = set(zlib.decompress(base64.b64decode(text[2:-1])).decode('utf8').rstrip(' ').split(' '))
	for w in words:
		if not w in d:
			d[w] = []
		d[w].append(num)
		#print(w, num, sep='\t')

for i in d.keys():
	print(i, ' '.join(map(str, d[i])), sep='\t')

