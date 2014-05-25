import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import listdir
from os.path import isfile, join


import os
CURR_DIR = os.path.dirname(os.path.dirname(__file__))

BASE_URL = "http://www.scopus.com"
READ_PATH = os.path.join(CURR_DIR, "UniquePapers.txt")
#folder_paths = {"2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012"}
DEST_PATH = CURR_DIR

def extractReferences(papername):
	references = []
	# start a new instance of Firefox
	driver = webdriver.Firefox()
	driver.get(BASE_URL)
	#try:
	# search for the paper on scopus
	elem = driver.find_element_by_id("searchterm1")
	elem.send_keys(papername)
	elem.send_keys(Keys.ENTER)
	time.sleep(2)
	# go through the search results
	paper_results_list = driver.find_elements_by_class_name("dataCol2")	# list of papers
	conference_results_list = driver.find_elements_by_class_name("dataCol5")	# where the corresponding paper was presented
	i = 0
	paper_link = ""
	for paper in paper_results_list:
		conf_presented = conference_results_list[i].text
		try:
			if(((conf_presented.find("DETC") > -1) and (conf_presented.find("Proceedings") > -1)) or ((conf_presented.find("ASME") > -1) and (conf_presented.find("Proceedings") > -1)) or (conf_presented.find("International Design Engineering Technical Conferences and Computers and Information in Engineering") > -1)):
				#print(conf_presented)
				paper.find_element_by_tag_name("a").click()
				break
		except ValueError:
				i += 1
				continue
		i += 1
	time.sleep(2)
	#elem = results_list.find_element_by_tag_name("a")
	#paper_link.click()
	# extract references
	
	# generate a bibliography for the document	NOT WORKING
	#doc_results_list = driver.find_element_by_id("docResultList")
	#doc_results_list.find_element_by_name("selectAllCheckBox").click()
	#a_refs = doc_results.find_elements_by_tag_name("a")
	#for ref in a_refs:
	#	if "bibliography" in ref.text:
	#		ref.click()
	#		break
	
	#reference_list = driver.find_element_by_class_name("referenceLists")
	reference_blks = driver.find_elements_by_class_name("referencesBlk")
	#print("found ", len(reference_blks))
	for reference_blk in reference_blks:
		reference_title = ''
		try:
			ref_title = reference_blk.find_element_by_class_name("refDocTitle")
			reference_title = ref_title.find_element_by_tag_name('a').text
			#print(reference_title)
		except Exception as e:
			#print(e.strerror)
			#print("Searching for 'em' tag")
			try:
				reference_title = reference_blk.find_element_by_tag_name('em').text
				#print(reference_title)
			except Exception as e1:
				#print("Didn't find 'em' tag")
				continue
		references.append(reference_title)
	#finally:
	driver.close()
	# return the list of references
	return references

def examinePapers():
	reference_paper_list = open(DEST_PATH + "list_of_references.txt", "a")
	pprs_file = open(READ_PATH, "r")
	i = 0
	print(i)
	for line in pprs_file:
		i += 1
		if(i <= 900):
			continue
		references = extractReferences(line[:line.index("#") - 1])
		reference_paper_list.write((line[:line.index("#") - 1]) + " ")
		for ref in references:
			if(len(ref) <= 1):
				continue
			try:
				reference_paper_list.write("#" + ref)
			except Exception as e:
				continue
		reference_paper_list.write("\n")
		#if(i == 900):
		#	break
		time.sleep(2)
	print("done for " + (str)(i))

examinePapers()
