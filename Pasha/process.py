import spellcheck
import snippet

def process(s):
	q = s.lower().split()
	q_ed = spellcheck.spell(q)
	modif = False
	if q != q_ed and q_ed is not None:
		print(q, q_ed)
		modif = ' '.join(q_ed)
		print(modif)
		print('Modified!!!')
	else:
		print('Not modified')

	urls = ['ololo.fm'] * 6
	ans = [(['железнодорожн', 'вокзал', 'в', 'качеств', 'диспле', 'для', 'показ', 'реклам', 'он', 'поступ',
		'в', 'продаж', '21', 'сентябр'], 100)] * 6
	s = snippet.snip(ans)
	snippets = []
	for i in range(len(s)):
		a = {}
		a['url'] = urls[i]
		a['text'] = s[i][0]
		a['title'] = s[i][1]
		a['image'] = s[i][2]
		snippets.append(a)
	return snippets, modif

if __name__ == '__main__':
	process()