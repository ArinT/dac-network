from __future__ import division
import json

# f = open ('corpus.txt','r')
f = open ('topics.txt','r')
data = f.read().split('\n')

output = {}

for i in range (0,len(data)):

	topics_line = data[i]
	topic_array = topics_line.split(",")[:-1]
	total_words = len(topic_array)
	topic_hash_count = {}

	for t in topic_array:
		t = int(t)
		if t in topic_hash_count:
			topic_hash_count[t] += 1
		else:
			topic_hash_count[t] = 1

	#normalize the topic distribution
	for key in topic_hash_count:
		value = topic_hash_count[key]
		topic_hash_count[key] = value / total_words

	for j in range(0,8):
		if j not in topic_hash_count:
			topic_hash_count[j] = 0.00
	output[i] = topic_hash_count

with open ('document_topic_distribution.txt', 'w') as outfile:
	json.dump(output, outfile)
print "dumped, done"
