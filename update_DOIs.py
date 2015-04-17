#!/usr/bin/env python

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
from network_visualizer.models import Papers
import json
#import re
#import urllib2
#from urllib import quote

with open("DAC_Entire_Database.json") as f:
	data = json.load(f)
	f.close()

for i in xrange(len(data)):
	article = data[i]
	paper = Papers.objects.get(title=article["Title"])
	doi = article["DOI"][4:]
	paper.doi = doi
	paper.save()
	


"""search_url = "http://api.elsevier.com/content/search/scopus?query=title({0})&apiKey=40fcc70c0c0d4bccc9c94ac25f5d14a9&htmlAccept=application/json"
unfound_papers = []
for i in xrange(456, len(Papers.objects.all())):
	print i
	if i % 100 == 0:
		print unfound_papers
	paper = Papers.objects.all()[i]
	# print paper.paperid
	# print paper.title
	# print paper.doi
	# exit()
	title = paper.title
	title = re.sub(r'([^\s\w])+', ' ', title)
	title = quote(title)
	real_url = search_url.format(title)
	#print real_url
	response = urllib2.urlopen(real_url)
	data = response.read()
	response.close()
	parsed_response = json.loads(data)
	try:
		if parsed_response["search-results"]["opensearch:totalResults"] == str(0):
			unfound_papers.append(paper.paperid)
			continue
		doi = parsed_response["search-results"]["entry"][0]["prism:doi"]
	except KeyError:
		unfound_papers.append(paper.paperid)
		continue
	paper.doi = doi
	paper.save()
print unfound_papers"""