import json
from pprint import pprint
import os
import re

try:
  import cPickle as pickle
except:
  print "exception"
  import pickle

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
from network_visualizer.models import Papers, Works, Authors, AuthorTopics, Citations, Topfives, SimilarAuthors



pkl_file = open('/Users/yishh/Downloads/ranked_similar_authors.pkl', 'rb')
ranked_array = pickle.load(pkl_file)
pkl_file.close()

index = 2
#971
for i in range(0, len(ranked_array)):
	index += 1
	print "i: ", i
	p_id = ranked_array[i][0]
	ranks = ranked_array[i][1]
	top_10 = ranks[:10]
	top_10 = [x[0] for x in top_10]
	# print top_10
	# break

	for j in range(len(top_10)):
		# print i, j
		r1 = SimilarAuthors.objects.create( parentid = p_id, childid = top_10[j], rank = j+1)
		# r1.save()

		# parentid = models.IntegerField(db_column='parentId', blank=True, null=True) # Field name made lowercase.
  #   childid = models.IntegerField(db_column='childId', blank=True, null=True) # Field name made lowercase.
  #   rank = models.IntegerField(blank=True, null=True)
  #   _id
	# paper.save()
# print ranked_array[0]
print "added top10s"
