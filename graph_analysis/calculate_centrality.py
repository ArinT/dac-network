__author__ = 'arin'
from networkx.readwrite import json_graph
from networkx.algorithms import centrality
import json


def calculate_all_centralities():
    data = json.load(open("../static/json/authors.json"))
    G = json_graph.node_link_graph(data)
    degree = centrality.degree_centrality(G)
    closeness = centrality.closeness_centrality(G)
    betweeness = centrality.betweenness_centrality(G)
    #eigenvector = centrality.eigenvector_centrality(G)
    degree_max = -1
    closeness_max = -1
    betweeness_max = -1
    for item in degree:
        if item>degree_max:
            degree_max = item
    for item in closeness:
        if item>closeness_max:
            clo_max = item
    for item in betweeness:
        if item>betweeness_max:
            betweeness_max = item
    for item in degree:
        item = item/degree_max
    for item in closeness:
        item = item/closeness_max
    for item in betweeness:
        item = item/betweeness_max
    for author in data['nodes']:
        i = author['id']
        author['degreeCentrality'] = degree[i]
        author['closenessCentrality'] = closeness[i]
        author['betweennessCentrality'] = betweeness[i]

    writer = open("../static/json/authors_centrality.json", "w+")
    writer.write(json.dumps(data))


calculate_all_centralities()