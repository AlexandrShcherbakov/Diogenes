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
	for i in s.encode('utf8'):
		res *= p
		res += i
		res %= mod
	return res

def get_links(ind):
	return [links[i] for i in ind]
	for i in ind:
		print(links[i])
	print(len(ind), "sites showed")


stem = Stemmer.Stemmer('russian')
pagemap = [i.split('\t') for i in open('/media/alex/Seagate Backup Plus Drive/IR/project/page_map.txt', 'r').readlines()]
pagemap = [[i[0], int(i[1]), int(i[2])] for i in pagemap]
hashtblfile = open('/media/alex/Seagate Backup Plus Drive/IR/project/Step4/map.txt', 'r')
hashtbl = []
for i in hashtblfile.readlines():
	i1 = i.split('\t')
	if len(i1) > 1:
		hashtbl.append([int(i1[0]), i1[1], int(i1[2]), int(i1[3])])
	else:
		hashtbl.append([0])
hashtblfile.close()
binfl = open('/media/alex/Seagate Backup Plus Drive/IR/project/Step4/dict', 'rb')
links = [0] + list(map(lambda x: x.split('\t')[1][:-1], open('/media/alex/Seagate Backup Plus Drive/IR/all/urls.txt').readlines()))
	
#get_query
#query to list of words
#stemming for list of words
def queryToStemmedList(query):
	words = query.rstrip('\n').split(' ')
	words = list(set(map(lambda x: x.lower(), words)))
	st_words = list(map(lambda x: stem.stemWord(x), filter(lambda x: len(x) > 2, words)))
	return [words, st_words]
#bool search for each word
#join indexes
def boolSearch(st_terms):
	index = onlyANDquery(st_terms)
	return index

def onlyANDquery(query):
	print(query)
	lenindex = []
	ind = get_index(query[0])
	lenindex.append(len(ind))
	for i in range(1, len(query)):
		ind2 = get_index(query[i])
		lenindex.append(len(ind2))
		ind = index_AND(ind, ind2)
	return ind, lenindex

def index_AND(ind1, ind2):
	i = 0
	j = 0
	res = []
	while j < len(ind2):
		while i < len(ind1) and ind1[i] < ind2[j]:
			i += 1
		if i == len(ind1):
			break
		if ind1[i] == ind2[j]:
			res.append(ind1[i])
		j += 1
	return res

def get_index(word):
	hs = myhash(word)
	print(hs)
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
		num = num[0] * 256 ** 3 + num[1] * 256 ** 2 + num[2] * 256 + num[3]
		nums += [num]
	res = simple9decode(nums)
	zer = len(res) - 1
	while zer != 0 and res[zer] == 0:
		zer -= 1
	res = res[:zer + 1]
	for i in range(1, len(res)):
		res[i] += res[i - 1]
	return res

#compute bm25 for index
#take top 100
def compute_BM25(st_terms, index, lenindex):
	#compute idfs
	max_urls = len(links)
	idfs = [log(max_urls / lenindex[i]) for i in range(len(st_terms))]
	#compute BM25
	resdocs = PriorityQueue(101)
	for i in range(len(index)):
		doc = loaddoc(index[i])
		bm = -sum([BM25(st_terms[j], doc, idfs[j]) for j in range(len(st_terms))])
		if resdocs.full():
			resdocs.get()
		resdocs.put((bm, [index[i], doc]))
	res = []
	while not resdocs.empty():
		res.append(list(resdocs.get()))
	result = [[-i[0], i[1][0], i[1][1]] for i in res[:101]]
	return result, idfs

def loaddoc(num):
	num -= 1
	fl, offset, size = pagemap[num]
	fl = open('/media/alex/Seagate Backup Plus Drive/IR/project/' + fl, 'rb')
	fl.seek(offset)
	return fl.read(size).decode('utf-8').lower().split(' ')

#compute passages
#take top 6
def compute_passages(top100, st_terms, idfs):
	pas = []
	parameters = [2, 0.25, 0.75]
	for i in top100:
		pas.append(passage_algorithm(i[2], st_terms, idfs, parameters))
	comose_parameters = [0.5, 0.5]
	for i in range(len(top100)):
		top100[i][0] *= comose_parameters[1]
		top100[i][0] += pas[i][0] * comose_parameters[0]
		top100[i].append(pas[i][1])
	top6 = sorted(top100, reverse=True)[:6]
	inds = [i[1] for i in top6]
	passages = [i[-1] for i in top6]
	return inds, passages


def holy_shit(q):
	a = queryToStemmedList(q)
	b = boolSearch(a[1])
	if len(b[0]) == 0:
		return []
	c = compute_BM25(a[1], b[0], b[1])
	d = compute_passages(c[0], a[1], c[1])
	print(d[1])
	return get_links(d[0])