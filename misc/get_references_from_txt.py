__author__ = 'arin'
TEXT_DIR = "/home/arin/Desktop/DACOfficialTextDocs/"
PAPERS_FILE = "/home/arin/thesis/DAC_network_analysis/misc/papers.json"
WRITE_FILE = "/home/arin/Desktop/paps.json"
import json, os, re
def get_all_reference(paper_file, dir):
    papers = json.load(open(paper_file))
    i = 0

    for paper in papers:
        for file in os.listdir(dir):
            if file.split(".txt")[0] == paper['doi']:
                filename = TEXT_DIR+file
                refs =extract_references_from_txt(filename)
                if len(refs)!=0:
                    i+=1
                paper['references']=refs
    writer = open(WRITE_FILE,'w+')
    writer.write(json.dumps(papers))
    print i
def extract_references(text):
    open = u"\u201C"
    close = u"\u201D"
    matches=re.findall(r''+open+'(.+?)'+close+'',text.decode('UTF-8',errors='replace'))
    return matches
def extract_references_from_txt(filename):
    file = open(filename)
    references_section = ""
    references_section_found = False
    for line in file:
        if "REFERENCES" ==line[0:10]:
            references_section_found = True
        if references_section_found:
            references_section+=line + " "
    references_section = references_section.replace('\n','')
    refs = extract_references(references_section)
    return refs
# get_all_reference(PAPERS_FILE,TEXT_DIR)