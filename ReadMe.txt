Files:
	1. BigStemmer.py - used to convert all htmls to lists of stemmed words
		stdin - lenta.ru
		stdout - stemmed words
	2. mapper.py - used to build reverse index from lists of stemmed words
		stdin - stemmed words
		stdout - reverse index
	3. reducer.py - used to compress index by simple9
		stdin - reverse index
		stdout - compressed index
	4. dal.py - used to create hashtable and binary file with reverse index
		stdin - compressed index
		stdout - progress information
		dict - writed binary reverse index
		map.txt - writed hashtable with offsets and sizes of reverse indexes
	5. index.html - frontend
	6. styles.css - styles for index.html
