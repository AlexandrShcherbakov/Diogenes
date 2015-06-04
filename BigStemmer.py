#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import zlib
import sys
import re
import Stemmer

for line in sys.stdin:
	number, data = line.split('\t')
	html_text = zlib.decompress(base64.b64decode(data)).decode('utf-8')
	#soup = bs4.BeautifulSoup(html_text)
	#for i in range(len(soup.findAll('script'))):
	#	soup.script.decompose()
	#text = soup.get_text()
	ind = html_text.find('<script')
	while ind != -1:
		rind = html_text.find('</script>')
		html_text = html_text[:ind] + html_text[rind + 9:]
		ind = html_text.find('<script')
	text = re.sub('<[^>]*>', ' ', html_text)
	words = re.findall(re.compile(r'[\w]+', re.U), text)
	words = list(filter(lambda x: len(x) > 2, words))
	st = Stemmer.Stemmer('russian')
	words = list(map(lambda x: st.stemWord(x.lower()), words))
	words = ' '.join(words)
	result = base64.b64encode(zlib.compress(words.encode('utf8')))
	print(number, result, sep='\t')
	if int(number) % 1000 == 0:
		sys.stderr.write(number + '\n')