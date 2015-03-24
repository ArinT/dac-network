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
		print self.author_id, " ", self.author_name, " ", self.papers, " ", self.coauthors
# for p in paper_corpus:
# 	paper_corpus[p].self_print()


author_memo = {}

#first add in all the papers to an author
with open('../author_coauthor_paper_map.csv', 'rb') as csvfile:
	title_reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
	i = 0
	for row in title_reader:
		if i == 0:
			i += 1
			continue
		row = row[0]
		author_name = doit(row)
		row = row.split(",")
		author_id = int(row[0])
		co_author_id = int(row[1])
		paper_id = int(row[2])

		#add new author if not existing
		if author_id not in author_memo:
			#create new author object
			new_author = author(author_id, author_name)
		else:
			new_author = author_memo[author_id]
		#add paper if not already there
		if paper_id not in new_author.papers:
			#retrieve paper object
			p1 = paper_corpus[paper_id]
			#put paper into author
			new_author.papers[paper_id] = p1
		

			# #add coauthor if not already there
			# if coauthor_id not in new_author.coauthors:

		author_memo[author_id] = new_author
		# print author_id, co_author_id, paper_id, author_name
# print author_memo

print "added in papers"
#next add in all coauthors of an author

with open('../author_coauthor_paper_map.csv', 'rb') as csvfile:
	title_reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
	i = 0
	for row in title_reader:
		if i == 0:
			i += 1
			continue
		row = row[0]
		author_name = doit(row)
		row = row.split(",")
		author_id = int(row[0])
		co_author_id = int(row[1])
		paper_id = int(row[2])

		#retrieve author object
		a1 = author_memo[author_id]
		if co_author_id not in a1.coauthors:
			#retrive coauthor object
			c1 = author_memo[co_author_id]
			#add it c1 to coauthors of a1
			a1.coauthors[co_author_id] = c1
			author_memo[author_id] = a1

print "building coauthors"
print "size of author memo: ", len(author_memo)

output = open('authors.pkl', 'wb')
pickle.dump(author_memo, output)
output.close()

# with open('authors.txt', 'w') as outfile:
#     json.dump(author_memo, outfile)
for key in author_memo:
	author_memo[key].self_print()


'sql query to get the coauthor papers table is below'
'''
Create view author_paper_map as
SELECT 
    Authors.AuthorID , AuthorName,PaperID
FROM
    Authors join Works on Authors.AuthorID = Works.AuthorID;

SELECT 
    author_paper_map.AuthorID AS author_id,
    Works.AuthorId AS coauthor_id,
    author_paper_map.PaperID AS paper_id,
	author_paper_map.AuthorName AS author_name
FROM
    author_paper_map
        JOIN
    Works ON author_paper_map.PaperID = Works.PaperID
WHERE
    author_paper_map.AuthorID != Works.AuthorId
ORDER BY author_id asc	,paper_id asc
'''