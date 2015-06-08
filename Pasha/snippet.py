#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#from __future__ import print_function
import base64
import zlib
import sys
import re

def ends(s):
	res = [0] * len(s)
	for i in range(len(s) - 3):
		if s[i] == '?' or s[i] == '!':
			res[i] = 1
		elif s[i] == '.' and s[i - 2] != ' ' and s[i + 1] == ' ' and not s[i + 2].islower():
				res[i] = 1
	return res


def get(req, title, url):
	#path = './1_1000/'
	path = '/media/pavel/Seagate Backup Plus Drive/IR/all/'
	f = open(path + 'shift.txt', 'r')
	fl = {}
	sh = {}
	for i in f.readlines():
		t = i.split()
		x = int(t[0])
		if x in req:
			#print(i)
			fl[x] = t[1]
			sh[x] = int(t[2])
	f.close()
	for i in req.keys():
		f = open(path + fl[i], 'r')
		f.seek(sh[i])
		number, data = f.readline().split('\t')
		f.close()
		html_text = zlib.decompress(base64.b64decode(data)).decode('utf-8')
		
		x = re.search('<title>.*</title>', html_text).span()
		t = html_text[x[0] + 7: x[1] - 8]
		while t.find(':') > 0:
			t = t[t.find(':') + 1:]
		title[i] = t

		try:
			x = html_text.find('b-topic__title-image')
			if x >= 0:
				y = re.search('src="[^"]*"', html_text[x : x + 1000]).span()
				url[i] = html_text[x + y[0] + 5 : x + y[1] - 1]
			else:
				x = html_text.find('data-image')
				if x > 0:
					y = re.search('"url":"[^"]*"', html_text[x : x + 1000]).span()
					url[i] = html_text[x + y[0] + 7 : x + y[1] - 1]
		except:
			pass

		if i not in url:
			url[i] = 'http://img0.ask.fm/assets2/073/450/118/400/normal/stLfazm.jpg'

		html_text = re.sub('</?h[^>]*>', '. ', html_text)
		ind = html_text.find('<script')
		while ind != -1:
			rind = html_text.find('</script>')
			html_text = html_text[:ind] + html_text[rind + 9:]
			ind = html_text.find('<script')
		text = html_text
		text = re.sub('<script.*</script>', '', html_text)
		text = re.sub('</?h[^>]*>', '. ', text)
		text = re.sub('<[^>]*>', ' ', text)
		#text = text.replace('\n', ' ')
		text = re.sub('[\s]+', ' ', text)
		text = text.replace(' .', '.')
		req[i] = text
		#print(text)

def snip(lst, length=100):
	req = {}
	title = {}
	url = {}
	for i in lst:
		req[i[1]] = ''
	get(req, title, url)
	res = []
	for t in lst:
		i = 2
		pos = -1
		text = req[t[1]]
		#print(text)
		while True:
			temp = '.{,%d}' % i
			temp = temp.join(t[0])
			#print(temp)
			x = re.search(temp, text, re.IGNORECASE)
			if x:
				pos = x.span()[0]
				break
			else:
				i += 1
		#print(pos)
		dots = ends(text)
		r = ''
		p = pos
		while (not dots[p - 1]) and (pos - p < 100) and (p > 10):
			p -= 1
		if not dots[p - 1]:
			while text[p - 1] != ' ':
				p -= 1
		pos = p
		for i in range(pos + length, pos + length + 100):
			if dots[i]:
				r = text[pos : i]
				break
		i = pos + length
		while r == '':
			i += 1
			if text[i] == ' ':
				r = text[pos : i]
		r = r.strip()
		res.append((r, title[t[1]], url[t[1]]))
		#print(r)
		#print(title[t[1]])
		#print(url[t[1]])
		#print()
	return res

def main():
	#req = [(['железнодорожн', 'вокзал', 'в', 'качеств', 'диспле', 'для', 'показ', 'реклам', 'он', 'поступ',
	#	'в', 'продаж', '21', 'сентябр'], 100)]
	#req = [(['игра'], i) for i in range(41, 42)]
	req = [[['медвед', 'владимир', 'путин', 'выступ', 'с', 'послан', 'к', 'федеральн', 'собран', 'в', 'четверг', '4'], 453128], [['медвед', 'призва', 'голосова', 'за', 'един', 'росс', 'и', 'путин', 'главн', 'росс', 'мир', 'бывш', 'ссср', 'финанс', 'бизнес', 'силов', 'структур'], 477134], [['путин', 'об', 'эт', 'медвед', 'заяв', 'в', 'интерв', 'трем', 'федеральн', 'канал', '29', 'сентябр', 'если'], 88304], [['медвед', 'пообеща', 'избав', 'росс', 'от', 'ненужн', 'импорт', 'lenta', 'ru', '10', 'декабр', '2014', 'путин', 'назва', 'рост', 'цен', 'на', 'продукт', 'времен', 'lenta', 'ru', '09'], 261248], [['медвед', 'захват', 'проходн', 'комбинат', '00', '21', 'сегодн', 'путин', 'рассказа', 'о', 'рецепт', 'счастлив', 'нов', 'год', '14', '44', '30'], 30763], [['медвед', 'был', 'водвор', 'обратн', 'в', 'зоопарк', 'обсуд', 'последн', 'новост', '13', '42', 'путин', 'поддержа', 'выделен', 'земл', 'жител', 'дальн', 'восток', '13', '50', 'подсчита'], 332445]]
	print(snip(req))

if __name__ == '__main__':
	main()