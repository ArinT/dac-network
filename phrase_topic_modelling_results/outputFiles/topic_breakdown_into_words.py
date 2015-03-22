from __future__ import division

# f = open ('corpus.txt','r')
f = open ('corpus.txt','r')



data = f.read().split('\n')
for i in (0,len(data)):
	topics_line = data[i]
	topic_array = topics_line.split(",")[:-1]
	total_words = len(topic_array)
	print topic_array
	topic_hash_count = {}

	for t in topic_array:
		t = int(t)
		if t in topic_hash_count:
			topic_hash_count[t] += 1
		else:
			topic_hash_count[t] = 1



	print topic_hash_count

	#normalize the topic distribution
	for key in topic_hash_count:
		value = topic_hash_count[key]
		topic_hash_count[key] = value / total_words

	print topic_hash_count
	break