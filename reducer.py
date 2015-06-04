#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

def get_variant(nums):
	variants = [[1, 28], [4, 14], [8, 9], [16, 7], [32, 5], [128, 4], [512, 3], [16384, 2], [268435456, 1]]
	for i in range(len(variants)):
		if all(map(lambda x: x <= variants[i][0], nums[:variants[i][1]])):
			return i

def simple9encode(nums):
	variants = [[1, 28], [2, 14], [3, 9], [4, 7], [5, 5], [7, 4], [9, 3], [14, 2], [28, 1]]
	i = 0
	res = []
	while i < len(nums):
		var = get_variant(nums[i:i + 28])
		res.append(var)
		if i + variants[var][1] > len(nums):
			nums += [0] * (i + variants[var][1] - len(nums))
		for j in range(i, i + variants[var][1]):
			res[-1] <<= variants[var][0]
			res[-1] += nums[j]
		res[-1] <<= 28 - variants[var][0] * variants[var][1]
		i += variants[var][1]
	return res

last_word = ''
doc_nums = []
it = 0
for line in sys.stdin:
	word, nums = line.split('\t')
	doc_nums = sorted([int(i) for i in nums.split(' ')])
	for i in range(len(doc_nums) - 1, 0, -1):
		doc_nums[i] -= doc_nums[i - 1]
	result = simple9encode(doc_nums)
	print(word + '\t' + ' '.join(map(str, result)))