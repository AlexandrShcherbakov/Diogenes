#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def myhash(s, p=257, mod=2**64):
	res = 0
	for i in s:
		res *= p
		res += ord(i)
		res %= mod
	return res

print 'Dal started'
it = 0
hashs = []
offset = 0
dictionary = open('dict', 'wb')
for line in sys.stdin:
	ln = line.rstrip('\t\n').split('\t')
	if len(ln) < 2:
		continue
	nums = list(map(int, ln[1].split(' ')))
	hashs.append([myhash(ln[0]), ln[0], offset, len(nums) * 4])
	for n in nums:
		k = 24
		while k >= 0:
			dictionary.write(chr((n >> k) & 255))
			k -= 8
	offset += 4 * len(nums)
	it += 1
	if it % 1000 == 0:
		print(it, 'words saved')
dictionary.close()
l = len(hashs) * 2
hashtbl = [0] * l
maxq = 0
for i in hashs:
	pos = i[0] % l
	q = 0
	while hashtbl[pos] != 0:
		pos = (pos + 1) % l
		q += 1
	hashtbl[pos] = i
	if maxq < q:
		maxq = q
		print maxq
hstblfile = open('map.txt', 'w')
for h in hashtbl:
	if h == 0:
		hstblfile.write('\n')
	else:
		hstblfile.write('\t'.join(map(str, h)) + '\n')
hstblfile.close()
print 'Dal finished'
print maxq