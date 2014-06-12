__author__ = 'arin'
from networkx.readwrite import json_graph
from networkx.algorithms import centrality
import json
import math

def calculate_all_centralities():
    data = json.load(open("../static/json/authors.json"))
    G = json_graph.node_link_graph(data)
    degree = centrality.degree_centrality(G)
    closeness = centrality.closeness_centrality(G)
    betweeness = centrality.betweenness_centrality(G)
    #eigenvector = centrality.eigenvector_centrality(G)
    degree_max = -1.0
    closeness_max = -1.0
    betweeness_max = -1.0
    for i in degree:
        if degree[i]>degree_max:
            degree_max = degree[i]
    for i in closeness:
        if closeness[i]>closeness_max:
            closeness_max = closeness[i]
    for i in betweeness:
        if betweeness[i]>betweeness_max:
            betweeness_max = betweeness[i]
    for i in degree:
        if degree[i] != 0:
            degree[i] = math.log(degree[i]/degree_max)
    for i in closeness:
        if closeness[i] != 0:
            closeness[i] = math.log(closeness[i]/closeness_max)
    for i in betweeness:
        if betweeness[i] != 0:
            betweeness[i] = math.log(betweeness[i]/betweeness_max)
    for author in data['nodes']:
        i = author['id']
        author['degreeCentrality'] = degree[i]
        author['closenessCentrality'] = closeness[i]
        author['betweennessCentrality'] = betweeness[i]

    writer = open("../static/json/authors_centrality.json", "w+")
    writer.write(json.dumps(data))


calculate_all_centralities()