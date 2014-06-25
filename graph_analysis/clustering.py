__author__ = 'arin'
import json
from networkx.algorithms.cluster import clustering
from networkx.readwrite import  json_graph
from networkx.classes.graph import Graph
from networkx.classes.digraph import DiGraph
def add_clustering_groups(infile, outfile):
    json_data = json.load(open(infile))
    multigraph = json_graph.node_link_graph(json_data)
    G = Graph()
    for node in multigraph.nodes_iter():
        G.add_node(node)
    for edge in multigraph.edges_iter():
        for existing_edge in G.edges_iter():
            if existing_edge[0] == edge[0] and existing_edge[1] == edge[1]:
                G.edge[edge[0]][edge[1]]['weight'] += 1
        G.add_edge(edge[0],edge[1], weight = 1)
    clusters  = clustering(G)
    for author in json_data['nodes']:
        author['clusteringCoefficient'] = clusters[author['id']]
    writer = open(outfile, "w+")
    writer.write(json.dumps(json_data))

add_clustering_groups("../static/json/authors_centrality.json","../static/json/authors_comp.json")