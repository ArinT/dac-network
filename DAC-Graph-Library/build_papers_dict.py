try:
	import cPickle as pickle
except:
	print "exception"
	import pickle

import json
import csv
import sys

class paper:
	def __init__(self, title, doi, url, year, abstract, topic_dist):
		
		self.title = title
		self.doi = doi
		self.url = url
		self.year = year
		self.abstract = abstract
		self.topic_dist = topic_dist

		self.authors = {}
		self.paper_id = ""

	def self_print(self):
		print self.paper_id, " ", self.title, " ", self.doi, " ", self.url, " ", self.year, " ", self.authors, " ", self.topic_dist
		print self.abstract

json_data=open('../DAC_Entire_DataBase.json')
data = json.load(json_data)

titles_data_json = open('../titles_in_db.txt')
titles_data = json.load(titles_data_json)

topic_dist_json = open('../phrase_topic_modelling_results/outputFiles/document_topic_distribution.txt')
topic_dist_data = json.load(topic_dist_json)
print "topic dist data: ", len(topic_dist_data)
paper_corpus = {}
print (len(data))
for i in range (0,len(data)):

	paper_1 = data[i]
	doi = paper_1["DOI"][4:]
	doi = ("").join([unicode(s).encode("utf-8") for s in doi])
	title = paper_1["Title"]
	title = ("").join([unicode(s).encode("utf-8") for s in title])
	url = paper_1["URL"]
	url = ("").join([unicode(s).encode("utf-8") for s in url])
	topics = paper_1["Topics"]
	year = paper_1["Year"]
	authors = paper_1["Authors"]
	abstract = paper_1["Abstract"]
	abstract = ("").join([unicode(s).encode("utf-8") for s in abstract])

	topic_dist = topic_dist_data[str(i)]

	topic_dist_array = []
	for k in topic_dist:
		topic_dist_array.append( (int(k),topic_dist[k]) )

	topic_dist_array = sorted(topic_dist_array, key = lambda x : x[0])

	p = paper(title, doi, url, year, abstract, topic_dist_array)

	paper_corpus[title] = p


print "initial paper_corpus"
# print paper_corpus.keys()
print " "

def doit(text):
	'this extracts things from double quotes'
	import re
	matches=re.findall(r'\"(.+?)\"',text)
	return ",".join(matches)


with open('../paperid_titles_map.csv', 'rb') as csvfile:
	count_i = 0
	title_reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
	i = 0
	for row in title_reader:
		if i == 0:
			i += 1
			continue

		row_norm = row[0]
		
		row = row_norm.split(",")
		paper_id = row[0]
		title = doit(row_norm)
		doi = row[2]
		url = row[3]

		if title in paper_corpus:
			paper_corpus[title].paper_id = paper_id
			paper_temp = paper_corpus[title]
			paper_corpus[int(paper_id)] = paper_temp
			del(paper_corpus[title])
		else:
			count_i += 1
			print title


print "missing papers: ", count_i
print "done adding in paper ids"

#now instantiate the authors
print "corpus keys"
print paper_corpus.keys()
print "size of paper corpus: ", len(paper_corpus)


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


# write python dict to a file
output = open('papers.pkl', 'wb')
pickle.dump(paper_corpus, output)
output.close()

# # read python dict back from the file
# pkl_file = open('myfile.pkl', 'rb')
# mydict2 = pickle.load(pkl_file)
# pkl_file.close()

