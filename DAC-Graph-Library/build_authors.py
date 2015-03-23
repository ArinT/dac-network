try:
	import cPickle as pickle
except:
	print "exception"
	import pickle

import json
import csv
import sys
from build_papers_dict import paper, doit

pkl_file = open('papers.pkl', 'rb')
paper_corpus = pickle.load(pkl_file)
pkl_file.close()

class author:
	'common base class for all authors'
	def __init__(self, author_id, author_name):
		self.author_id = author_id
		self.author_name = author_name
		self.papers = {}
		self.coauthors = {}

	def self_print(self):
		print self.author_id, " ", self.author_name, " ", self.papers, " ", self.authors
# for p in paper_corpus:
# 	paper_corpus[p].self_print()

with open('../authors_papers_map.csv', 'rb') as csvfile:
	title_reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
	i = 0
	for row in title_reader:
		if i == 0:
			i += 1
			continue
		row = row[0]
		author_name = doit(row)
		row = row.split(",")
		author_id = row[0]
		paper_id = row[-1]

		# print author_id, author_name, paper_id
		paper_id = int(paper_id)
		# print paper_corpus[paper_id]
		paper_corpus[paper_id].authors[author_id] = 1