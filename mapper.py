#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import base64
import zlib

d = {}

it = 0

for line in sys.stdin:
	num, text = line.rstrip('\n').split('\t')
	num = int(num) + 1
	dec_text = zlib.decompress(base64.b64decode(text[2:-1])).decode('utf8').rstrip(' ').split(' ')
	words = {}
	for word in dec_text:
		if not word in words:
			words[word] = 9000000000 + num
		words[word] -= 1000000
		#words.append([word, dec_text.count(word) * 1000000 + num])
	for w in words.keys():
		if not w in d:
			d[w] = []
		d[w].append(words[w])
		#print(w, num, sep='\t')
	it += 1
	if it % 1000 == 0:
		sys.stderr.write(str(it) + '\n')

sys.stderr.write('Read complete')
it = 0

for i in sorted(d.keys()):
	print(i, ' '.join(map(str, d[i])), sep='\t')
	it += 1
	if it % 1000 == 0:
		sys.stderr.write(str(it) + '\n')	

