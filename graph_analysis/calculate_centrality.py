__author__ = 'arin'
from networkx.readwrite import json_graph
from networkx.algorithms import centrality
from networkx.classes.digraph import DiGraph
from networkx.exception import NetworkXError
import json

def calculate_all_centralities(data):
    G = json_graph.node_link_graph(data)
    degree = centrality.degree_centrality(G)
    closeness = centrality.closeness_centrality(G)
    betweeness = centrality.betweenness_centrality(G)
    eigenvector_fail = False
    try:
        eigenvector = centrality.eigenvector_centrality(DiGraph(G),max_iter=100000)
    except NetworkXError:
        eigenvector = []
        eigenvector_fail = True
        print "Max iterations exceeded"
    degree_max = -1.0
    closeness_max = -1.0
    betweeness_max = -1.0
    eigenvector_max = -1.0
    for author in data['nodes']:
        i = author['id']
        author['degreeCentralityUnnormalized'] = degree[i]
        author['closenessCentralityUnnormalized'] = closeness[i]
        author['betweennessCentralityUnnormalized'] = betweeness[i]
        author['eigenvectorCentralityUnnormalized'] = eigenvector[i] if not eigenvector_fail else 1.0

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
        author['eigenvectorCentrality'] = eigenvector[i] if not eigenvector_fail else 1.0
    return data