# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import epub
import index
import lexems
import config

def intersect(lhs, rhs):
	i, j = 0, 0
	n, m = len(lhs), len(rhs)
	result = []
	while i < n and j < m:
		d = lhs[i] - rhs[j]
		if d == 0:
			result.append(lhs[i])
			i +=1; j += 1
		elif d < 0:
			i += 1
		else:
			j += 1
	return result

def search(keywords, idx):
	
	def size_cmp(lhs, rhs):
		return len(lhs) - len(rhs)
	
	keywords = lexems.get(keywords)
	docs = []
	for keyword in keywords:
		docs.append(idx.docids(keyword.lower()))
	
	if len(docs) == 0:
		return docs
	
	docs.sort(size_cmp)
	
	docids = docs[0]
	for i in xrange(1, len(docs)):
		docids = intersect(docids, docs[i])
		
	return docids

def printResult(docs):
	for file_name in docs:
		info = epub.Info(file_name)
		print (', '.join(info.authors()).strip() + '.', ', '.join(info.titles()).strip() + '. (' + file_name + ')')

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print ('Usage: python', sys.argv[0], 'dir [keywords]')
		os._exit(os.EX_USAGE)
	
	idx = index.Index(sys.argv[1].decode(config.SystemCodePage))
	
	if len(sys.argv) > 2:
		keywords = []
		for i in xrange(2, len(sys.argv)):
			keywords.append(sys.argv[i].decode(config.SystemCodePage))
		docs = search(' '.join(keywords), idx)
		printResult(docs)
		os._exit(os.EX_OK)

	print ('press Ctrl-D to exit')
	while True:
		try:
			keywords = raw_input('# ').decode(config.SystemCodePage)
		except EOFError:
			print ('')
			break
		docids = search(keywords, idx)
		docs = [idx.document(docid) for docid in docids]
		printResult(docs)
