import numpy as np

try:
	import cPickle as pickle
except:
	print "exception"
	import pickle

import json,csv, sys
# from build_papers_dict import paper, doit
from build_authors import author

#obtain pathsim scores
W_pathsim = np.load("pathsim.npy")

#load index to id dictionary
pkl_file = open('author_index_memo.pkl', 'rb')
author_index_memo = pickle.load(pkl_file)
pkl_file.close()

#load index to id array
pkl_file_2 = open('author_index_array.pkl', 'rb')
author_index_array = pickle.load(pkl_file_2)
pkl_file_2.close()

#load author objects dict
pkl_file_3 = open('authors.pkl', 'rb')
author_memo = pickle.load(pkl_file_3)
pkl_file_3.close()


peer_array = []

def get_author_name(ind):
	author_obj = author_memo[ind]
	return author_obj.author_name


# peer_file = open("peers.txt", "w")


top_X_num = 10
for i in range (len(W_pathsim)):
	current_author_id = author_index_array[i]
	author_name = get_author_name(current_author_id)
	pathsim_i = W_pathsim[i]
	
	#remap author names and index back
	# pathsim_i = [(pathsim_i[index],get_author_name(author_index_array[index])) for index in range(len(pathsim_i))]
	# pathsim_i = [(pathsim_i[index],get_author_name(author_index_array[index])) for index in range(len(pathsim_i))]
	pathsim_i = [(author_index_array[index],pathsim_i[index]) for index in range(len(pathsim_i))]
	pathsim_sorted = sorted(pathsim_i, key = lambda x: x[1] , reverse = True)
	# pathsim_sorted = [x[1] for x in pathsim_sorted]
	
	temp_list = pathsim_sorted[:(top_X_num+1)]
	
	#remove self index
	top_X = []
	for a in temp_list:
		if a[0] == current_author_id:
			continue
		top_X.append(a)
	top_X = top_X[:top_X_num]
	peer_array.append((current_author_id,top_X))
	# print peer_array
	# break
	# author_string = str(current_author_id) + " " + author_name + "\n"
	# author_string = " ---- " + author_name + " ---- \n"
	# peer_file.write(author_string)
	# top_X_string = str(top_X) + "\n"
	# peer_file.write(top_X_string)

# peer_file.close()
print "time to pickle your peer_authors"
output = open('ranked_similar_authors.pkl', 'wb')
pickle.dump(peer_array, output)
output.close()

print "similar authors pickled. \n"
	# if i == 100:
	# 	break

