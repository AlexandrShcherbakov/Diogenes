#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from sys import stdin, argv
from glob import glob

def main():
	if len(argv) < 2:
		print('llooool')
		return
	g = open(argv[1] + 'shift.txt', 'w')
	for fl in glob(argv[1] + '/docs-*.txt'):
		f = open(fl, 'r')
		pos = 0
		for i in f.readlines():
			g.write('%s %s %d\n' % (i.split()[0], fl[len(argv[1]):], pos))
			pos += len(i)
	g.close()

if __name__ == '__main__':
	main()