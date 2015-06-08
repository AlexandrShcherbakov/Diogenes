# -*- coding: utf-8 -*-

from bottle import route, run, template, request
import process

scolors = ['#ffa07a', '#f4c480', '#F0E68C', '#98FB98', '#AFEEEE', '#D8BFD8']


@route('/')
def index():
	query = request.query.query
	if query == '':
		return template('startpage')
	#snippets = [{'title' : 'Ололо', 'url' : 'vk.com', 'text' : '<b>ololo</b> ololo', 'image' : 'ololo.jpg'}] * 6
	snippets, modif = process.process(query)
	if modif:
		query = modif
	return template('index', query=query, snippets=snippets, scolors=scolors, modif=modif)
		
if __name__ == "__main__":
	run(host='0.0.0.0', port=8080, debug=True)
