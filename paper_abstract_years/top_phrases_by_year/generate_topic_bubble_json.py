import json

phrase_memo = {}

for i in range (0, 13):
	year = 2002 + i
	f_name = 'topPhrases_' + str(year) + '.txt'

	f = open(f_name)
	f = f.read().split('\n')
	f = f[:-1]

	temp_array = []
	for line in f:
		line = line.split('\t')
		# print line
		phrase = line[0]
		count = (int(line[1]) +2)* 4 

		if phrase not in phrase_memo:
			phrase_memo[phrase] = [(year,count)]
		else:
			phrase_memo[phrase].append((year,count))

# print phrase_memo
#now the dict is constructed
phrase_json = []

for key in phrase_memo:
	total_sum = 0
	new_entry = {"articles" : [[2002,0],[2003,0],[2004,0],[2005,0],[2006,0],[2007,0],[2008,0],[2009,0],[2010,0],[2011,0],[2012,0],[2013,0],[2014,0]], "total":0, "name": key}
	year_count_array = phrase_memo[key]
	for value in year_count_array:
		year = value[0]
		count = value[1]
		total_sum += count
		year_index = year - 2002
		new_entry["articles"][year_index] = [year,count]
	new_entry["total"] = total_sum
	# print new_entry
	phrase_json.append(new_entry)
# [
#   {
#     "articles": [
#       [
#         2008,
#         9
#       ],
#       [
#         2009,
#         6
#       ],
#       [
#         2010,
#         3
#       ],
#       [
#         2011,
#         9
#       ],
#       [
#         2012,
#         21
#       ],
#       [
#         2013,
#         34
#       ]
#     ],
#     "total": 82,
#     "name": "Brain stimulation"
#   },



with open ('test_timeline.json', 'wb') as outfile:
	json.dump(phrase_json, outfile)