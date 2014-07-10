__author__ = 'arin'
import json,os,re
import fuzzy
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
from django.db import connection

TEXT_DIR = "/home/arin/Desktop/DACOfficialTextDocs/"
PAPERS_FILE = "/home/arin/thesis/DAC_network_analysis/misc/papers.json"
PAPERS_WITH_REFERENCES_FILE =  "/home/arin/thesis/DAC_network_analysis/misc/papers_with_references.json"
REFERENCES_FILE = "/home/arin/thesis/DAC_network_analysis/misc/references.json"
STOP_WORDS = [':', ' on ',' in ',' the ',' and ',' of ',' by ',' as ',' to ',' at ',' a ',' and ',' for ',' an ',' to ', '-']

def remove_stopwords(text):
    text = " "+text
    text = text.upper()
    for word in STOP_WORDS:
        text = text.replace(word.upper()," ")
    return text
def get_citations(filename, outfile):
    papers = json.load(open(filename))
    edges = []
    i = 1
    for source in papers:
        print "doon", i
        i += 1
        soundex = fuzzy.Soundex(25)
        for reference in source['references']:
            for target in papers:
                s = remove_stopwords(reference.encode('UTF-8'))
                t = remove_stopwords(target['title'].encode('UTF-8'))
                if soundex(s) == soundex(t):
                    edges.append({'source': source['doi'], 'target': target['doi']})
    print len(edges)
    writer = open(outfile, "w+")
    writer.write(json.dumps(edges))
def insert_into_citation_table(filename):
    citations = json.load(open(filename))
    cursor = connection.cursor()
    cursor.execute(
        'DROP TABLE IF EXISTS Citations;'
        'CREATE TABLE Citations(sourcePaperId INT, targetPaperId INT, citationId INT NOT NULL AUTO_INCREMENT PRIMARY KEY);'
    )
    cursor.close()
    i = 0

    for citation in citations:
        print i
        i+=1
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO Citations (sourcePaperId, targetPaperId) VALUES '
            '((SELECT PaperId FROM Papers WHERE DOI = %s),(SELECT PaperId FROM Papers WHERE DOI = %s));'
            ,[citation['source'].encode('UTF-8'),citation['target'].encode('UTF-8')])
        cursor.close()
def add_references_to_papers(infile, outfile, dir):
    papers = json.load(open(infile))
    i = 0

    for paper in papers:
        for file in os.listdir(dir):
            if file.split(".txt")[0] == paper['doi']:
                filename = TEXT_DIR+file
                refs =extract_references_from_txt(filename)
                paper['references']=refs
    writer = open(outfile,'w+')
    writer.write(json.dumps(papers))
def extract_references(text):
    open = u"\u201C"
    close = u"\u201D"
    undir_quote_strs = re.findall(r'\"(.+?)\"',text.decode('UTF-8', errors = 'replace'))
    dir_quote_strs=re.findall(r''+open+'(.+?)'+close+'',text.decode('UTF-8',errors='replace'))
    if len(undir_quote_strs) > len(dir_quote_strs):
        return undir_quote_strs
    return dir_quote_strs
def extract_references_from_txt(filename):
    file = open(filename)
    references_section = ""
    references_section_found = False
    for line in file:
        if "REFERENCES"  in line:
            references_section_found = True
        if references_section_found:
            references_section+=line + " "
    references_section = references_section.replace('\n','')
    refs = extract_references(references_section)
    return refs

add_references_to_papers(PAPERS_FILE,PAPERS_WITH_REFERENCES_FILE, TEXT_DIR)
get_citations(PAPERS_WITH_REFERENCES_FILE,REFERENCES_FILE)
insert_into_citation_table(REFERENCES_FILE)
