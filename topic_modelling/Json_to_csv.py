__author__ = 'arin'
import json


def json_to_csv():
    file = open("top5recommendationsinorder.txt")
    json_data = json.load(file)
    writer = open("top5.csv", "a")
    for parent in json_data:
        parent_list = json_data[parent]
        i = 1
        for child in parent_list:
            writer.write(parent.encode("UTF-8")+","+child.encode("UTF-8")+","+str(i)+"\n")
            i += 1
json_to_csv()
