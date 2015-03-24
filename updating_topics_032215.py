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





# print len(data)

# paper = data[1010:1011]
# for p in paper:
# 	# print p['Title']
# 	print p

# exit()

for i in range (0,len(data)):
	# print i
	paper = data[i]
	title = paper["Title"].encode('utf-8')
	# url = paper["URL"]
	# url = ("").join([unicode(s).encode("utf-8") for s in url])
	topics = paper["Topics"]
	# year = paper["Year"]
	# authors = paper["Authors"]
	print "Title: ", title
	abstract = paper["Abstract"]
	if abstract is not None:
		abstract = abstract.encode('utf-8')

	p1 = Papers.objects.filter(title=title)

	if len(p1):
		p1 = p1[0]
		p1.abstract = abstract
		paper_id = p1.paperid

		for t in topics:
			t = t.encode('utf-8')
			print "topic: ", t, ",paper id: ", paper_id
			t_set = Topics.objects.filter(topic = t)
			if len(t_set) == 0:
				t_1 = Topics.objects.create(topic = t, paperid = paper_id)
				t_1.save()
			else:
				current_t = t_set[0]

			

		# p1.save()
		print "updated topic: ", i
		# break
	else:
		continue

	# abstract = abstract.encode('utf-8')
	# numauthors = len(authors)
	# isASME = 1
	# isDAC = 1
	# PublicationName = "DAC Conference " + str(year)
	# pages = int(re.findall("\(.* pages\)", paper_id)[0].split()[0][1:])

	# paper = Papers.objects.create( doi = doi, title = title, url = url,
	#  year = year , pages = pages, numauthors = numauthors,
	# 	isasme = 1, isdac = 1, publicationname = PublicationName)
	# # paper.save()
	# print abstract
	"topics updated"
	print i
	# if i == 10:
	# 	break
	# for a in authors:
	# 	a = ("").join([unicode(s).encode("utf-8") for s in a])
	# 	print a, "author name"
	# 	author_id = Authors.objects.get(authorname = a)
	# 	work = Works.objects.create(authorid=author_id.authorid, paperid=paper.paperid)
	# 	work.save()
	# 	print "saved author"

















# ("").join([unicode(s).encode("utf-8") for s in author['url']])
	# for topic in topics:


	# for author in authors:
	# 	work = Works.objects.create(authorid=author.authorid, paperid=paper.paperid)
 #        work.save()


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

# pprint(data)
json_data.close()




