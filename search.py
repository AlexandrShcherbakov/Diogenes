#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from math import log
from ranklib import *
import base64
import zlib
import re
from queue import PriorityQueue
import Stemmer

def simple9decode(nums):
	variants = [[1, 28], [2, 14], [3, 9], [4, 7], [5, 5], [7, 4], [9, 3], [14, 2], [28, 1]]
	result = []
	for i in nums:
		var = variants[i >> 28]
		k = (var[1] - 1) * var[0]
		zeros = 28 - var[0] * var[1]
		while k >= 0:
			result.append(((i >> (k + zeros)) & ((1 << var[0]) - 1)))
			k -= var[0]
	return result

def simple9decode1(num):
	variants = [[1, 28], [2, 14], [3, 9], [4, 7], [5, 5], [7, 4], [9, 3], [14, 2], [28, 1]]
	result = []
	var = variants[num >> 28]
	k = (var[1] - 1) * var[0]
	zeros = 28 - var[0] * var[1]
	while k >= 0:
		result.append(((num >> (k + zeros)) & ((1 << var[0]) - 1)))
		k -= var[0]
	zer = len(result) - 1
	while zer != 0 and result[zer] == 0:
		zer -= 1
	return result[:zer + 1]

def myhash(s, p=257, mod=2**64):
	res = 0
	for i in s:
		res *= p
		res += ord(i)
		res %= mod
	return res

def get_index(word):
	if word.startswith('NOT'):
		word = word[3:]
	word = word.decode('utf-8').lower().encode('utf-8')
	hs = myhash(word)
	l = len(hashtbl)
	pos = hs % l
	stpos = pos
	while hashtbl[pos][0] != hs or hashtbl[pos][1] != word:
		pos = (pos + 1) % l
		if pos == stpos:
			return []
	binfl.seek(int(hashtbl[pos][2]))
	nums = []
	for i in range(0, int(hashtbl[pos][3]), 4):
		num = binfl.read(4)
		num = ord(num[0]) * 256 ** 3 + ord(num[1]) * 256 ** 2 + ord(num[2]) * 256 + ord(num[3])
		nums += [num]
	if len(sys.argv) > 1 and sys.argv[1] == 'fib':
		res = fib_decode(nums, fb)
	else:
		res = simple9decode(nums)
	zer = len(res) - 1
	while zer != 0 and res[zer] == 0:
		zer -= 1
	res = res[:zer + 1]
	for i in range(1, len(res)):
		res[i] += res[i - 1]
	return res

def index_AND(ind1, ind2):
	if len(ind1) == 0 or len(ind2) == 0:
		return []
	res = []
	i = 0
	j = 0
	while True:
		while i < len(ind1) and j < len(ind2) and ind1[i] < ind2[j]:
			i += 1
		while i < len(ind1) and j < len(ind2) and ind1[i] > ind2[j]:
			j += 1
		if i >= len(ind1) or j >= len(ind2):
			break
		res.append(ind1[i])
		i += 1
		j += 1
	return res

def index_ANDNOT(ind1, ind2):
	if not len(ind2):
		return ind1
	res = []
	i = 0
	j = 0
	while True:
		while i < len(ind1) and j < len(ind2) and ind1[i] < ind2[j]:
			res.append(ind1[i])
			i += 1
		while i < len(ind1) and j < len(ind2) and ind1[i] > ind2[j]:
			j += 1
		if i >= len(ind1) or j >= len(ind2):
			if i < len(ind1):
				res += ind1[i:]
			break
		i += 1
		j += 1
	return res

def index_NOTAND(ind1, ind2):
	return index_ANDNOT(ind2, ind1)

def index_OR(ind1, ind2):
	return list(set(ind1 + ind2))

def get_links(ind):
	for i in ind:
		print(links[i])
	print(len(ind), "sites showed")

def onlyORquery(query, q1):
	ind = q1[0]
	for i in range(1, len(query)):
		ind2 = q1[i]
		ind = index_OR(ind, ind2)
	return ind

def onlyANDquery(query):
	indexes = []
	if query[0].startswith('NOT'):
		sgn1 = -1
	else:
		sgn1 = 1
	ind = get_index(query[0])
	indexes.append(ind)
	for i in range(1, len(query)):
		if query[i].startswith('NOT'):
			sgn2 = -1
		else:
			sgn2 = 1
		ind2 = get_index(query[i])
		indexes.append(ind2)
		if sgn1 < 0:
			ind = index_NOTAND(ind, ind2)
			sgn1 = 1
		else:
			if sgn2 < 0:
				ind = index_ANDNOT(ind, ind2)
			else:
				ind = index_AND(ind, ind2)
	return ind, indexes

def calculate_query():
	query = sys.stdin.readline()[:-1]
	terms = query.split(' ')
	q, indexes = onlyANDquery(terms)
	if len(q) != 0:
		res = range_result(terms, q, indexes)
	else:
		print("0 pages was found.")
	#qusplOR = query.split(' OR ')
	#qusplAND = [list(map(lambda x: x.replace(' ', ''), i.split(' AND '))) for i in qusplOR]
	#q1 = [onlyANDquery(x) for x in qusplAND]
	#get_links(onlyORquery(qusplAND, q1), links)

def loaddoc(num):
	for i in range(len(pagemap)):
		if num >= pagemap[i][0]:
			break
	f = open(pagemap[i][1], 'r')
	for j in range(num - pagemap[i][0]):
		f.readline()
	doc = re.findall(re.compile("\w+", re.U), zlib.decompress(base64.b64decode(f.readline().split('\t')[1])).decode('utf-8').lower())
	doc = list(map(lambda x: x.encode('utf-8'), doc))
	alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
	doc = list(filter(lambda x: x[0] in alphabet, doc))
	return doc

def range_result(terms, alldocs, indexes):
	print(len(alldocs), 'pages was found')
	#compute idfs
	max_urls = 570000
	idfs = [log(max_urls / len(indexes[i])) for i in range(len(terms))]
	#compute BM25
	resdocs = PriorityQueue(101)
	for i in range(len(alldocs)):
		doc = loaddoc(alldocs[i])
		bmparams = [float(sys.argv[7]), float(sys.argv[8])]
		bm = sum([BM25(terms[j], doc, idfs[j]) for j in range(len(terms))])
		if resdocs.full():
			resdocs.get()
		resdocs.put((bm, [alldocs[i], doc]))
	res = []
	while not resdocs.empty():
		res.append(list(resdocs.get()))
	pas = []
	parameters = [float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])]
	for i in res:
		pas.append(passage_algorithm(i[1][1], terms, idfs, parameters))
	for i in range(len(res)):
		res[i][0] *= params[1]
		res[i][0] += pas[i] * params[0]
	res = sorted(res)[:10]
	inds = [i[1][0] for i in res]
	get_links(inds)


def main():
	params = [float(sys.argv[1]), float(sys.argv[2])]
	pagemap = [i.split('\t')[::-1] for i in open('page_map.txt', 'r').readline().split('\n')[:-1]]
	pagemap = [[int(i[0]), i[1]] for i in pagemap][::-1]
	fb = calculate_fib()
	hashtblfile = open('map.txt', 'r')
	hashtbl = []
	for i in hashtblfile.readlines():
		i1 = i.split('\t')
		if len(i1) > 1:
			hashtbl.append([int(i1[0]), i1[1], int(i1[2]), int(i1[3])])
		else:
			hashtbl.append([0])
	hashtblfile.close()
	binfl = open('dict', 'rb')
	links = [0] + list(map(lambda x: x.split('\t')[1][:-1], open('1_1000/urls.txt').readlines()))
	while True:
		print('Enter your query, please:')
		calculate_query()

stem = Stemmer.Stemmer('russian')
#get_query
#query to list of words
#stemming for list of words
def queryToStemmedList(query):
	words = query.rstrip('\n').split(' ')
	words = list(set(map(lambda x: x.lower(), words)))
	st_words = list(set(map(lambda x: stem.stemWord(x), filter(lambda x: len(x) > 2, words))))
	return [words, st_words]
#bool search for each word

#join indexes
#compute bm25 for index
#take top 100
#compute passages
#take top 6