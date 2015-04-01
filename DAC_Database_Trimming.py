import csv
import json

json_data=open('DAC_Entire_DataBase.json')
data = json.load(json_data)

title_memo = {}

with open('titles_in_db.csv', 'rb') as csvfile:
	title_reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
	# print len(title_reader)
	# title_reader = title_reader[1:]
	i = 0
	for row in title_reader:
		if i == 0:
			i += 1
			continue
		# row = row[1:]
		# row = row[:-1]
		# print ', '.join(row)
		row = row[0]
		row = row[1::]
		title = row[:-1]
		# print title
		title_memo[title] = 1
		i += 1
		# if i == 10:
		# 	break
# print title_memo

with open("titles_in_db.txt",'w') as outfile:
	json.dump(title_memo,outfile)