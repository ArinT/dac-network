__author__ = 'arin'
import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
from django.db import connection
from network_visualizer.models import Papers, Authors, Citations
from graph_analysis.clustering import add_clustering_communities
from graph_analysis.calculate_centrality import calculate_all_centralities
OUTFILE = 'citations.json'
def get_year(doi):
    return int(doi[4:8])


def paper_is_cited_or_cites(citation, paper):
    return citation.sourcepaperid == paper.paperid or citation.targetpaperid == paper.paperid


def generate_citation_network_json( year ):
    citations = Citations.objects.all()
    papers = Papers.objects.all()
    node_set = set()
    edges = []
    nodes = []
    for paper in papers:
        for citation in citations:
            if paper_is_cited_or_cites(citation, paper) and year>= get_year(paper.doi):
                node_set.add(paper)
    for paper in node_set:
        nodes.append({'id':paper.paperid,'name':paper.title,'doi':paper.doi})
    for citation in citations:
        source = -1
        target = -1
        for i in range (0,len(nodes)):
            if citation.sourcepaperid == nodes[i]['id']:
                source = i
            if citation.targetpaperid ==  nodes[i]['id']:
                target = i
        if target !=-1 and source !=-1:
            edges.append({'source':source,'target':target})
    json = {'nodes':nodes,'links':edges}
    return json
def get_collaborations():
    cursor = connection.cursor()
    cursor.execute('SELECT w1.AuthorId, w2.AuthorId, SUBSTRING(p.DOI,5,4) FROM Works w1 '
                   'JOIN Works w2 ON w1.PaperId = w2.PaperId '
                   'JOIN Papers p ON w2.PaperId = p.PaperID '
                   'WHERE w1.AuthorId > w2.AuthorId')
    return cursor.fetchall()
def generate_author_network_json( year):
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
            paper_year = int(collaboration[2])
            if year >= paper_year:
                edges.append({'source':source, 'target':target})
    json = {'nodes':nodes, 'links':edges}
    return json
def write_json_to_file(outfile, j):
    writer = open(outfile,'w+')
    writer.write(json.dumps(j))


def create_and_analyze_network(year, outfile, type):
    generate  = [generate_author_network_json,generate_citation_network_json]
    author_network_json = generate[type](year)
    print ("Author" if type == 0 else "Citation")+" Network generated for "+str(year)
    author_network_json_with_centrality = calculate_all_centralities(author_network_json)
    print ("Author" if type == 0 else "Citation")+" Network centrality calculated for "+str(year)
    complete_author_network_json = add_clustering_communities(author_network_json_with_centrality)
    print ("Author" if type == 0 else "Citation")+" Network community clustering calculated for "+str(year)
    write_json_to_file(outfile, complete_author_network_json)
    print "Complete "+("Author" if type == 0 else "Citation")+" Network written to "+outfile
def main():
    create_and_analyze_network(2012,"/home/arin/Desktop/authors.json",0)
    create_and_analyze_network(2012,"/home/arin/Desktop/citations.json",1)
    for i in range (0,10):
        create_and_analyze_network(2002+i,"/home/arin/Desktop/yearly_authors/authors"+str(2002+i)+".json",0)
        create_and_analyze_network(2002+i,"/home/arin/Desktop/yearly_citations/citations"+str(2002+i)+".json",1)
main()
