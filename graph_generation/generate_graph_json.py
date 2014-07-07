__author__ = 'arin'
import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
from django.db import connection
from network_visualizer.models import Papers, Authors, Citations
def generate_citation_network_json():
    citations = Citations.objects.all()
    papers = Papers.objects.all()
    node_set = set()
    edges = []
    nodes = []
    for paper in papers:
        for citation in citations:
            if citation.sourcepaperid == paper.paperid or citation.targetpaperid == paper.paperid:
                node_set.add(paper)
    for paper in node_set:
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
def get_collaborations():
    cursor = connection.cursor()
    cursor.execute('SELECT w1.AuthorId, w2.AuthorId, SUBSTRING(p.DOI,5,4) FROM Works w1 '
                   'JOIN Works w2 ON w1.PaperId = w2.PaperId '
                   'JOIN Papers p ON w2.PaperId = p.PaperID '
                   'WHERE w1.AuthorId > w2.AuthorId')
    return cursor.fetchall()
def generate_author_network_json():
    authors = Authors.objects.all()
    nodes = []
    edges = []
    collaborations = get_collaborations()
    for author in authors:
        nodes.append({'id': author.authorid, 'name':author.authorname})
    for collaboration in collaborations:
        source = -1
        target = -1
        for i in range(0, len(authors)):
            if authors[i].authorid == collaboration[0]:
                source = i
            if authors[i].authorid == collaboration[1]:
                target = i
        if target != -1 and source !=-1:
            year = collaboration[2]
            edges.append({'source':source, 'target':target, 'year':year})
    j = {'nodes':nodes, 'links':edges}
    writer = open('authors.json','w+')
    writer.write(json.dumps(j))
# generate_author_network_json()
generate_citation_network_json()
