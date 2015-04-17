try:
	import cPickle as pickle
except:
	print "exception"
	import pickle

import json
import csv
import sys, os
import numpy as np
from build_papers_dict import paper, doit
from build_authors import author
from scipy.spatial.distance import cosine

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
# from network_visualizer.models import Topfives, Papers, Works, Authors, AuthorTopics, Citations
# exit()
# sys.setrecursionlimit(150000)
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
		#lower the better
		cos_score = cosine(v1, v_t)


		sim_score_array.append((p_temp_id,cos_score))

	sim_score_array = sorted(sim_score_array, key = lambda x: x[1])
	sim_score_top_5 = sim_score_array[:4]

	# for i in range(len(sim_score_top_5)):
	# 	x = 1

	paper_corpus_sim_scores.append((p_id,sim_score_array))


# print paper_corpus_sim_scores

# for p in paper_corpus:
# 	paper_corpus[p].self_print()
# print paper_corpus

print "time to pickle your ranked similar papers"
output = open('ranked_similar_papers.pkl', 'wb')
pickle.dump(paper_corpus_sim_scores, output)
output.close()
print "pickled"

# print "topic papers pickled. \n"


