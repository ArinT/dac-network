__author__ = 'Arin'
import json
import fuzzy
file = open("papers.json")
papers = json.load(open("papers.json"))
edges = []
i =1
for source in papers:
    print "doon", i
    i+=1
    soundex = fuzzy.Soundex(100)
    for reference in source['references']:
        for target in papers:
            if soundex(reference.encode('UTF-8')) == soundex(target['name'].encode('UTF-8')):
                edges.append({'source':source['doi'],'target':target['doi']})
print len(edges)
writer = open("citations.json","w+")
writer.write(json.dumps(edges))

