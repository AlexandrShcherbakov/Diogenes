#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from os import listdir
from os.path import isfile, join

out = open(sys.argv[1], 'w')

fl = [open(sys.argv[2] + '/' + i, 'r') for i in list(filter(lambda x: x[0] == '0', listdir(sys.argv[2])))]
words = [i.readline().split('\t') for i in fl]
can = [True] * len(words)

def can_it(c):
	for i in c:
		if c:
			return True
	return False

it = 0

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
	out.write(min_word + '\t' + ' '.join(map(str, nums)) + '\n')
	it += 1
	if it % 1000 == 0:
		print(it)
out.close()
