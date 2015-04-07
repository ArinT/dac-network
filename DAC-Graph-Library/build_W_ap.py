#find the Author to Paper Relationship

import numpy as np

try:
	import cPickle as pickle
except:
	print "exception"
	import pickle

import json
import csv
import sys
# from build_papers_dict import paper, doit
from build_authors import author

pkl_file = open('authors.pkl', 'rb')
author_memo = pickle.load(pkl_file)
pkl_file.close()

pkl_file_2 = open('paper_topics.pkl', 'rb')
paper_corpus = pickle.load(pkl_file_2)
pkl_file_2.close()



paper_index_array = []
paper_index_memo = {}
paper_count = 0
for paper_id in paper_corpus:
	paper_index_array.append(paper_id)
	paper_index_memo[paper_id] = paper_count
	paper_count += 1

print "paper index array: "
print paper_index_array

num_papers = len(paper_index_array)

# print author_memo.keys()
# print len(author_memo)

author_index = 0
author_index_array = []
author_index_memo = {}
num_authors = len(author_memo)

for author_id in author_memo:
	author_index_array.append(author_id)
	author_index_memo[author_id] = author_index
	author_index += 1


print "author index array: "
print author_index_array

# author_memo[2].self_print()
#W_ap matrix
W_ap = np.zeros(shape=(num_authors,num_papers)) 

for i in range (len(author_index_array)):
	author_id = author_index_array[i]
	author_obj = author_memo[author_id]
	# print author_obj.papers
	paper_array = author_obj.papers.keys()
	#now remap paper_id to paper_index
	new_data_entry = np.zeros(num_papers)
	for paper_id in paper_array:
		paper_index = paper_index_memo[paper_id]
		new_data_entry[paper_index] = 1
		# print paper_index
	W_ap[i] = new_data_entry
	# print paper_array
	# break

# np.savetxt('W_ap_test.txt', W_ap)
np.save("W_ap",W_ap)


print W_ap
# print W_ap[17]
np.set_printoptions(threshold='nan')
# print W_ap[1]
print "W_ap done"


