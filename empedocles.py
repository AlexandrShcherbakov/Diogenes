#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from os import listdir
from os.path import isfile, join
from math import log

out = open(sys.argv[1], 'w')

fl = [open(sys.argv[2] + '/' + i, 'r') for i in list(filter(lambda x: x[0] == '0', listdir(sys.argv[2])))]
words = [i.readline().split('\t') for i in fl]
can = [True] * len(words)

def can_it(c):
	for i in c:
		if i:
			return True
	return False

it = 0
idf = 0

def BM25(number):
	ln = number // 10**12
	tf = max(number // 10 ** 6 % 10**5, 0.000000000000000001)
	num = number % 10**6
	val = tf * idf / (tf + 2 * (0.25 + ln / 1627 * 0.75))
	return [val, num]


while can_it(can):
	for i in range(len(can)):
		if can[i]:
			break
	min_word = words[i][0]
	for i in range(len(can)):
		if can[i] and words[i][0] < min_word:
				min_word = words[i][0]
	nums = []
	for i in range(len(can)):
		if can[i] and words[i][0] == min_word:
			nums += [int(j) for j in words[i][1].split(' ')]
			words[i] = fl[i].readline()
			if not words[i]:
				can[i] = False
			else:
				words[i] = words[i].split('\t')
	idf = len(nums) / 564549
	nums = sorted(list(map(BM25, nums)), reverse=True)
	for i in range(len(nums)):
		nums[i][0] = int(round((i + 1) / len(nums) * 250))
	for i in range(len(nums)):
		nums[i] = nums[i][0] * 10**6 + nums[i][1]
	out.write(min_word + '\t' + ' '.join(map(str, nums)) + '\n')
	it += 1
	if it % 1000 == 0:
		print(it)
out.close()
