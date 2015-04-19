import json

# {
#  "name": "flare",
#  "children": [
#   {
#    "name": "analytics",
#    "children": [
#     {
#      "name": "cluster",
#      "children": [
#       {"name": "AgglomerativeCluster", "size": 3938},
#       {"name": "CommunityStructure", "size": 3812},
#       {"name": "HierarchicalCluster", "size": 6714},
#       {"name": "MergeEdge", "size": 743}
#      ]
#     },
#     {
#      "name": "graph",
#      "children": [
#       {"name": "Betw

topicbubble = {"name" :"topicbubble" , "children" :[] }
# topicbubble = {}

for i in range (0, 8):
	# year = 2002 + i
	f_name = str(i) + '.txt'

	f = open(f_name)
	f = f.read().split('\n')
	f = f[:-1]

	temp_array = []
	for line in f:
		line = line.split('\t')
		# print line
		phrase = line[0]
		# count = (int(line[1]) +2)* 4 
		count = (int(line[1]) +3)*2
		temp_array.append({"name":phrase, "size":count})
	topicbubble["children"].append({"name" : i , "children" : temp_array })
	if i % 2 == 1:
		topicbubble["children"].append({"name" : i+100 , "children" : [{"name" : "dummy", "size": 0}] })
	# topicbubble["children"].append({"name" : i+500 , "children" : [{"name" : "dummy", "size": 0}] })
	# topicbubble["name" : i , "children" : temp_array })
	# print f

	# print f_name
print topicbubble

with open ('test_bubble_topics.json', 'wb') as outfile:
	json.dump(topicbubble, outfile)