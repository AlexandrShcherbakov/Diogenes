#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import base64
import zlib
import sys
import re
import Stemmer
import BeautifulSoup


for line in sys.stdin:
	number, data = line.split('\t')
	html_text = zlib.decompress(base64.b64decode(data)).decode("utf-8")
	soup = BeautifulSoup.BeautifulSoup(html_text)
	map(lambda x: x.extract(), soup.findAll('script'))
	text = ''.join([e for e in soup.recursiveChildGenerator() if isinstance(e,unicode)]).replace('&nbsp;', ' ').replace('&quot;', '\'')
	words = re.findall(re.compile("[\w\d]+", re.U), text)
	words = list(filter(lambda x: len(x) > 2, words))
	st = Stemmer.Stemmer('russian')
	words = list(map(lambda x: st.stemWord(x.lower()), words))
	words = ' '.join(words).encode('utf8')
	result = base64.b64encode(zlib.compress(words))
	print(number, result, sep='\t')