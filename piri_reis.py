#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from os import listdir
from os.path import isfile, join
import base64
import zlib
import re

buf = []

mp = open('page_map.txt', 'w')
it = 0
num = 1

for fl in listdir(sys.argv[1]):
	if fl.startswith("docs"):
		buf += open(sys.argv[1] + '/' + fl, 'r').readlines()
		print(fl + ' readed')
	while len(buf) >= 750:
		out = open(sys.argv[2] + '/' + str(it), 'wb')
		for i in range(750):
			number, data = buf[i].rstrip('\n').split('\t')
			html_text = zlib.decompress(base64.b64decode(data)).decode('utf-8')
			ind = html_text.find('<script')
			while ind != -1:
				rind = html_text.find('</script>')
				html_text = html_text[:ind] + html_text[rind + 9:]
				ind = html_text.find('<script')
			text = re.sub('<[^>]*>', ' ', html_text).replace('&nbsp;', ' ')
			text = ' '.join(re.findall(r'\w+', re.sub(r'&[^;]{2,6};', ' ', text)))
			offset = out.tell()
			out.write(text.encode('utf8'))
			mp.write(sys.argv[2] + '/' + str(it) + '\t' + str(offset) + '\t' + str(out.tell() - offset) + '\n')
			num += 1
		print(str(it) + ' writed')
		out.close()
		buf = buf[750:]
		it += 1
out = open(sys.argv[2] + '/' + str(it), 'wb')
for i in range(len(buf)):
	number, data = buf[i].split('\t')
	html_text = zlib.decompress(base64.b64decode(data)).decode('utf-8')
	ind = html_text.find('<script')
	while ind != -1:
		rind = html_text.find('</script>')
		html_text = html_text[:ind] + html_text[rind + 9:]
		ind = html_text.find('<script')
	text = re.sub('<[^>]*>', ' ', html_text).replace('&nbsp;', ' ')
	text = ' '.join(re.findall(r'\w+', re.sub(r'&[^;]{2,6};', ' ', text))) + '\n'
	offset = out.tell()
	out.write(text.encode('utf8'))
	mp.write(sys.argv[2] + '/' + str(it) + '\t' + str(offset) + '\t' + str(out.tell() - offset) + '\n')
	num += 1
mp.close()
