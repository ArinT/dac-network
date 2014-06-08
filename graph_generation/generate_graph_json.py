__author__ = 'arin'
import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
from network_visualizer.models import Citations
from network_visualizer.models import Papers
def generate_citation_network_json():
    citations = Citations.objects.all()
    papers = Papers.objects.all()
    nodes = []
    edges = []

    for paper in papers:
        for citation in citations:
            if citation.sourcepaperid == paper.paperid or citation.targetpaperid == paper.paperid:
                nodes.append({'paperid':paper.paperid,'title':paper.title,'doi':paper.doi})
    for citation in citations:
        source = -1
        target = -1
        for i in range (0,len(nodes)):
            if citation.sourcepaperid == nodes[i]['paperid']:
                source = i
            if citation.targetpaperid ==  nodes[i]['paperid']:
                target = i
        if target !=-1 and source !=-1:
            edges.append({'source':source,'target':target})
    j = {'nodes':nodes,'links':edges}
    writer = open('citations.json','w+')
    writer.write(json.dumps(j))
generate_citation_network_json()