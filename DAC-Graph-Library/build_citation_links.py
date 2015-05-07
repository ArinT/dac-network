import numpy as np

try:
  import cPickle as pickle
except:
  print "exception"
  import pickle

import json,csv, sys, os
from os.path import dirname


citations_graph_memo = {"nodes":[], "links" :[]}

paper_id_index_map = {}

#select PaperID, DOI, Year, url, Title from Papers 
with open('../papers.csv', 'rb') as csvfile:
	title_reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
	i = 0
	for row in title_reader:
		if i == 0:
			i += 1
			continue

		#clean the csv
		row = row[0]
		row = row.split(',')

		paper_id = int(row[0])
		DOI = row[1][8::]
		year = int(row[2])
		url = row[3]
		title = row[4]
		title = title[1:]
		title = title[:-1]

		temp_paper_dict = {
			   	  "doi": DOI,
			      "group": 2,
			      "closenessCentralityUnnormalized": 0.1,
			      "eigenvectorCentralityUnnormalized": 0.1,
			      "backbone": False,
			      "name": title,
			      "degreeCentralityUnnormalized": 0.1,
			      "degreeCentrality": 0.1,
			      "betweennessCentralityUnnormalized": 0.1,
			      "betweennessCentrality": 0.1,
			      "closenessCentrality": 0.1,
			      "id": paper_id,
			      "eigenvectorCentrality": 0.1,
			      "url" : url,
			      "year" : year}
		#remember index of paper_id
		paper_id_index_map[paper_id] = i -1
		#add it to nodes
		citations_graph_memo['nodes'].append(temp_paper_dict)
		# break
		i +=1

# print " "
# print paper_id_index_map

#select * from Citations join Papers where sourcePaperId = Papers.PaperID and Year <= 2014 for years

with open('../citations_links.csv', 'rb') as csvfile:
	title_reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
	i = 0
	for row in title_reader:
		if i == 0:
			i += 1
			continue
		row = row[0]
		row = row.split(',')
		#make it int
		row = [int(x) for x in row]

		source = row[0]
		target = row[1]
		
		try:
			source_index = paper_id_index_map[source]
			target_index = paper_id_index_map[target]
		except:
			continue
		
		# print source, " :source: ", source_index
		# print target, " :target: ", target_index
		temp_link = {"source" : source_index, "target" : target_index}
		citations_graph_memo['links'].append(temp_link)
		# break
print citations_graph_memo

with open('citations_test.json', 'w') as outfile:
    json.dump(citations_graph_memo, outfile)
