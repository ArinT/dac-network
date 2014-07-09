__author__ = 'arin'
import json
from networkx.algorithms.cluster import clustering
from networkx.algorithms.community import k_clique_communities
from networkx.readwrite import  json_graph
from networkx.classes.graph import Graph


# def get_clustering_coefficients(multigraph):
#     G = Graph()
#     for node in multigraph.nodes_iter():
#         G.add_node(node)
#     for edge in multigraph.edges_iter():
#         for existing_edge in G.edges_iter():
#             if existing_edge[0] == edge[0] and existing_edge[1] == edge[1]:
#                 G.edge[edge[0]][edge[1]]['weight'] += 1
#         G.add_edge(edge[0], edge[1], weight=1)
#     clusters = clustering(G)
#     return clusters

def add_clustering_communities(infile, outfile):
    json_data = json.load(open(infile))
    multigraph = json_graph.node_link_graph(json_data)
    # clusters = get_clustering_coefficients(multigraph)
    communities = k_clique_communities(multigraph,6)
    for node in json_data['nodes']:
        node['group'] = 0
    c = 1
    for community in communities:
        for id in community:
            for node in json_data['nodes']:
                if node['id'] == id:
                    node['group'] = c
        c+=1
    writer = open(outfile, "w+")
    writer.write(json.dumps(json_data))
def check_groups(infile):
    json_data = json.load(open(infile))
    group_count = []
    for i in range(0,36):
        group_count.append(0)
    for node in json_data['nodes']:
        group_count[node['group']]+=1
    print group_count

# add_clustering_communities("../static/json/authors_without_groups.json","../static/json/authors.json")
check_groups("../static/json/authors.json")