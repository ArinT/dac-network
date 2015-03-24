# from bs4 import BeautifulSoup
# from unidecode import unidecode
import json
from pprint import pprint
import os
import re
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
from network_visualizer.models import Papers, Works, Authors, AuthorTopics, Citations, Topics

json_data=open('DAC_Entire_DataBase.json')
data = json.load(json_data)
#topics and authors

count = 0

titles_data_json = open('titles_in_db.txt')
titles_data = json.load(titles_data_json)


for i in range (0,len(data)):
	# print i
	paper = data[i]
	title = paper["Title"].encode('utf-8')
	# url = paper["URL"]
	# url = ("").join([unicode(s).encode("utf-8") for s in url])
	topics = paper["Topics"]
	# year = paper["Year"]
	# authors = paper["Authors"]
	# print "Title: ", title

	
	if title not in titles_data:
		count += 1
		print "this is not here: ", title, " count: ", count
		continue




# {
    #     "PaperID": "DETC2014-34345 pp. V02AT03A001; (7 pages)", 
    #     "DOI": "doi:10.1115/DETC2014-34345", 
    #     "Title": "Electromagnetic Design of In-Vehicle Reactor Using a Level-Set Based Topology Optimization Method", 
    #     "URL": "http://proceedings.asmedigitalcollection.asme.org//proceeding.aspx?articleID=2090498", 
    #     "Topics": [
    #         "Design", 
    #         "Optimization", 
    #         "Vehicles", 
    #         "Topology", 
    #         "Application-Tailored Optimization Methods"
    #     ], 
    #     "DETC": "DETC2014-34345", 
    #     "Year": 2014, 
    #     "Broad_Topic": "Application-Tailored Optimization Methods", 
    #     "Authors": [
    #         "Shintaro Yamasaki", 
    #         "Atsushi Kawamoto", 
    #         "Akira Saito", 
    #         "Masakatsu Kuroishi", 
    #         "Kikuo Fujita"
    #     ], 
    #     "Abstract": "In this paper, we propose a level-set based topology optimization method for designing a reactor, which is used as a part of the DC-DC converter in electric and hybrid vehicles. Since it realizes a high-power driving motor and its performance relies on its component, i.e., reactor core, it is valuable to establish a reasonable design method for the reactor core. Boundary tracking type level-set topology optimization is suitable for this purpose, because the shape and topology of the target structure is clearly represented by the zero boundary of the level-set function, and the state variables are accurately computed using the zero boundary tracking mesh. We formulate the design problem on the basis of electromagnetics, and derive the design sensitivities. The derived sensitivities are linked with boundary tracking type level-set topology optimization, and as a result, a useful structural optimization method for the reactor core design problem is developed."
    # }

json_data.close()
titles_data_json.close()




