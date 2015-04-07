try:
	import cPickle as pickle
except:
	print "exception"
	import pickle

import json
import csv
import sys
import numpy as np
from build_papers_dict import paper, doit
from build_authors import author
from scipy.spatial.distance import cosine

sys.setrecursionlimit(150000)
# v1 = [1,2,3,4]
# v2 = [100000,-10000,3,4]

# print cosine(v1,v2)

# exit()
pkl_file = open('papers.pkl', 'rb')
paper_corpus = pickle.load(pkl_file)
pkl_file.close()

pkl_file_2 = open('authors.pkl', 'rb')
author_memo = pickle.load(pkl_file_2)
pkl_file_2.close()


paper_array = [(p_id,paper_corpus[p_id]) for p_id in paper_corpus]
paper_array = sorted(paper_array, key = lambda x : x[0])



paper_corpus_sim_scores = []

#anything below a distance of 0.10 will be considered a legal edge for a topic link
cosine_threshold = 0.10

for p_id in paper_corpus:
	paper = paper_corpus[p_id]
	topic_dist = paper.topic_dist
	topic_v = [x[1] for x in topic_dist]
	v1 = np.array(topic_v)

	sim_score_array = []

	for i in range (0,len(paper_array)):
		p_temp = paper_array[i]
		p_temp_id = p_temp[0]
		if p_id == p_temp_id:
			continue
		p_obj = p_temp[1]
		p_obj_topics = p_obj.topic_dist
		p_obj_topic_v = [x[1] for x in p_obj_topics]
		v_t = np.array(p_obj_topic_v)

		#can try other similarity functions in the future
		cos_score = cosine(v1, v_t)

		if cos_score < cosine_threshold:
			paper.topic_links[p_temp_id] = p_obj
	paper_corpus[p_id] = paper

	# 	sim_score_array.append((p_temp_id,cos_score))

	# sim_score_array = sorted(sim_score_array, key = lambda x: x[1])
	# paper_corpus_sim_scores.append((p_id,sim_score_array))


# for p in paper_corpus:
# 	paper_corpus[p].self_print()
# print paper_corpus
# print paper_corpus_sim_scores
print "time to pickle your toes"
output = open('paper_topics.pkl', 'wb')
pickle.dump(paper_corpus, output)
output.close()

print "topic papers pickled. \n"


