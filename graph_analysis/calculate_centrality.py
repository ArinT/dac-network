__author__ = 'arin'
from networkx.readwrite import json_graph
from networkx.algorithms import centrality
from networkx.classes.digraph import DiGraph
import json

def calculate_all_centralities(infile, outfile):
    data = json.load(open(infile))
    G = json_graph.node_link_graph(data)
    degree = centrality.degree_centrality(G)
    closeness = centrality.closeness_centrality(G)
    betweeness = centrality.betweenness_centrality(G)
    eigenvector = centrality.eigenvector_centrality(DiGraph(G),max_iter=1000)
    degree_max = -1.0
    closeness_max = -1.0
    betweeness_max = -1.0
    eigenvector_max = -1.0
    for i in degree:
        if degree[i]>degree_max:
            degree_max = degree[i]
    for i in closeness:
        if closeness[i]>closeness_max:
            closeness_max = closeness[i]
    for i in betweeness:
        if betweeness[i]>betweeness_max:
            betweeness_max = betweeness[i]
    for i in eigenvector:
        if eigenvector[i]>eigenvector_max:
            eigenvector_max = eigenvector[i]

    for i in degree:
        if degree[i] != 0:
            degree[i] = degree[i]/degree_max
    for i in closeness:
        if closeness[i] != 0:
            closeness[i] = closeness[i]/closeness_max
    for i in betweeness:
        if betweeness[i] != 0:
            betweeness[i] = betweeness[i]/betweeness_max
    for i in eigenvector:
        if eigenvector[i] != 0:
            eigenvector[i] = eigenvector[i]/eigenvector_max

    for author in data['nodes']:
        i = author['id']
        author['degreeCentrality'] = degree[i]
        author['closenessCentrality'] = closeness[i]
        author['betweennessCentrality'] = betweeness[i]
        author['eigenvectorCentrality'] = eigenvector[i]

    writer = open(outfile, "w+")
    writer.write(json.dumps(data))

calculate_all_centralities("../static/json/citations.json","/home/arin/thesis/citations.json")
# calculate_all_centralities("../static/json/authors.json","../static/json/authors_centrality.json")