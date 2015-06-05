from math import log

def term_frequency(term, doc):
	res = doc.count(term)
	if not res :
		return 0
	return 1 + log(res)

def tf_idf(term, doc, idf):
	return term_frequency(term, doc) * idf

def doc_len(doc):
	return len(list(filter(lambda x: x != ' ', doc)))

def BM25(term, doc, idf, params=[0.5, 0.5], L=0):
	tf = term_frequency(term, doc)
	if L == 0:
		L = doc_len(doc)
	return tf * idf / (tf + params[0] * (params[1] + L * (1 - params[1])))

def count_inverse(query, passage):
	inv = 0
	ipas = list(map(lambda x: query.index(x[0]), passage))
	for i in range(len(passage)):
		for j in range(i + 1, len(passage)):
			if ipas[i] > ipas[j]:
				inv += 1
	return inv

def passage_tfidf(passage, doc, idfs):
	return sum(list(map(lambda x: tf_idf(passage[x][0], doc, idfs[x]), range(len(passage)))))

def passage_algorithm(doc, terms, idfs, parameters):
	#Extract passages
	passages = []
	passage = []
	for inddocterm in range(len(doc)):
		if doc[inddocterm] in terms:
			for t in passage:
				if t[0] == doc[inddocterm]:
					passage.remove(t)
					break
			passage.append([doc[inddocterm], inddocterm])
			passages.append(passage)
	#Compute metrics
	L = float(doc_len(doc))
	m_value = 0
	best_pas = passages[0]
	for passage in passages:
		metric = []
		metric.append(passage_tfidf(passage, doc, idfs))
		metric.append(len(passage) / len(terms))
		metric.append(count_inverse(terms, passage))
		metric.append(1 - passage[0][1] / L)
		val = sum([metric[i] * parameters[i] for i in range(len(metric))])
		#val = reduce(lambda res, i: res + metric[i] * parameters[i], range(len(metric)))
		if m_value < val:
			m_value = val
			best_pas = passage
	lit = max(0, min(best_pas, key=lambda x: x[1])[1] - 5)
	rit = min(len(doc), max(best_pas, key=lambda x : x[1])[1] + 6)
	return m_value, doc[lit:rit]

