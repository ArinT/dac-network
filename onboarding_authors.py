import json
from pprint import pprint
import os
import re
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
from network_visualizer.models import Papers, Works, Authors, AuthorTopics, Citations

def clean_unicode(text):
	if isinstance(text, unicode):
		text = text.encode('utf-8')
	return text


location_json_data = open('authorsLocations.json')
author_json_data = open('authorTopicsRevised.json')

location_data = json.load(location_json_data)
author_data = json.load(author_json_data)


for author in author_data:
	# print author

	author_name = ("").join([unicode(s).encode("utf-8") for s in author['Author']])
	# print author_name

	author_url = ("").join([unicode(s).encode("utf-8") for s in author['url']])
	# print author_url

	author_entry = Authors.objects.create( authorname = author_name, url = author_url)

	
	# author_entry.save()

	# author_content = ("").join([unicode(s).encode("utf-8") for s in author['Content Type']])
	# print author_content
	# author_topics =  author['Topics']
	# print author_topics

# c = 0
# for loc in location_data:
# 	c += 1
# 	print loc['url']
# 	print loc['Paper']
# 	print loc['Authors']

# 	if c == 1:
		# break



	