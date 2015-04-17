# {
#   "nodes": [

# {
#   "degreeCentralityUnnormalized": 0.0025853154084798,
#   "group": 12,
#   "closenessCentralityUnnormalized": 0.034202045122289,
#   "eigenvectorCentralityUnnormalized": 5.8950625831927e-6,
#   "backbone": false,
#   "name": "Melissa Gardenghi",
#   "closenessCentrality": 0.42202742824827,
#   "degreeCentrality": 0.044247787610619,
#   "betweennessCentralityUnnormalized": 0,
#   "betweennessCentrality": 0,
#   "id": 1934,
#   "eigenvectorCentrality": 1.5142523358037e-5
# }
# ,..
# ],
#   "links": [
#     {
#       "source": 1,
#       "target": 0
#     },
#     {
#       "source": 1,
#       "target": 0
#     },
#       {
#       "source": 1933,
#       "target": 869
#     }
#   ]
# }

import numpy as np

try:
  import cPickle as pickle
except:
  print "exception"
  import pickle



import json,csv, sys, os
from os.path import dirname
# from build_papers_dict import paper, doit

# dgl_path = dirname(dirname(dirname(os.path.abspath(__file__))))
# sys.path.insert(0, dgl_path)
import build_authors

#obtain pathsim scores
#W_pathsim = np.load("pathsim.npy")

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

author_graph_memo = {"nodes":[], "links" :[]}

index = 1
for key in author_memo:
	author_temp = author_memo[key]
	temp_auth_dict = {
	  "degreeCentralityUnnormalized": 0.01,
	  "group": 0.01,
	  "closenessCentralityUnnormalized": 0.01,
	  "eigenvectorCentralityUnnormalized": 0.01,
	  "backbone": False,
	  "name": author_temp.author_name,
	  "closenessCentrality": 0.01,
	  "degreeCentrality": 0.01,
	  "betweennessCentralityUnnormalized": 0.01,
	  "betweennessCentrality": 0.01,
	  "id": author_temp.author_id,
	  "eigenvectorCentrality": 0.01 }


	author_graph_memo["nodes"].append(temp_auth_dict)

	coauthors = author_temp.coauthors
	#remap it back for d3js to linearize it
	for co_id in coauthors:
		author_graph_memo["links"].append({"source" : author_index_memo[author_temp.author_id],"target":author_index_memo[co_id]})

#now map it back to 

with open('authors_test.json', 'w') as outfile:
    json.dump(author_graph_memo, outfile)
# authors_json = json.dumps(author_graph_memo, ensure_ascii=False)


