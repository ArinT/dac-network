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
from build_papers_dict import paper, doit
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
W_ptp = np.zeros(shape=(num_papers,num_papers)) 



for i in range (len(paper_index_array)):

	paper_id = paper_index_array[i]
	paper_obj = paper_corpus[paper_id]
	# paper_obj.self_print()
	ptp_papers = paper_obj.topic_links

	new_data_entry = np.zeros(num_papers)

	for ptp_id in ptp_papers:
		paper_index = paper_index_memo[ptp_id]
		new_data_entry[paper_index] = 1

	#hard code itself back in, every paper is linked to itself through the meta path
	new_data_entry[i] = 1
	W_ptp[i] = new_data_entry



output = open('author_index_memo.pkl', 'wb')
pickle.dump(author_index_memo, output)
output.close()

output = open('author_index_array.pkl', 'wb')
pickle.dump(author_index_array, output)
output.close()

output = open('paper_index_memo.pkl', 'wb')
pickle.dump(paper_index_memo, output)
output.close()

output = open('paper_index_array.pkl', 'wb')
pickle.dump(paper_index_array, output)
output.close()







# np.savetxt('W_ptp_test.txt', W_ptp)
np.save('W_ptp',W_ptp)


print W_ptp
# print W_ptp[0]
# print W_ptp[15]
np.set_printoptions(threshold='nan')
# print W_ptp[1]

print "W_ptp done"


