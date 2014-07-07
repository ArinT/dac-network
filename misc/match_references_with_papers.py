__author__ = 'Arin'
import json
import fuzzy
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
                t = remove_stopwords(target['name'].encode('UTF-8'))
                if soundex(s) == soundex(t):
                    edges.append({'source': source['doi'], 'target': target['doi']})
    print len(edges)
    writer = open(outfile, "w+")
    writer.write(json.dumps(edges))
get_citations("/home/arin/Desktop/paps.json","/home/arin/Desktop/citations.json")
def check_citations(filename):
    papers = json.load(open(filename))
    refs = []
    for paper in papers:
        if paper['doi'] in ['DETC2005-84790','DETC2007-34698','DETC2010-28788','DETC2008-49823','DETC2010-29055','DETC2010-28887','DETC2011-48521']:
            for ref  in paper['references']:
                refs.append(ref)
    print refs
# check_citations("/home/arin/Desktop/paps.json")