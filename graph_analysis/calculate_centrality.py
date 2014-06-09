__author__ = 'arin'
from networkx.readwrite import json_graph
from networkx.algorithms import centrality
import json


def calculate_all_centralities():
    global data, G, s, t, u, i, author, writer
    data = json.load(open("../static/json/authors.json"))
    G = json_graph.node_link_graph(data)
    s = centrality.degree_centrality(G)
    t = centrality.closeness_centrality(G)
    u = centrality.betweenness_centrality(G)
    # v = centrality.eigenvector_centrality(G)

    for author in data['nodes']:
        i = author['id']
        author['degreeCentrality'] = s[i]
        author['closenessCentrality'] = t[i]
        author['betweennessCentrality'] = u[i]

    writer = open("../static/json/authors_centrality.json", "w+")
    writer.write(json.dumps(data))


calculate_all_centralities()