__author__ = 'arin'
import json
from networkx.algorithms.cluster import clustering
from networkx.algorithms.community import k_clique_communities
from networkx.readwrite import  json_graph
from networkx.classes.graph import Graph
from community import best_partition
from community import partition_at_level
def make_nonmultigraph(multigraph):
    G = Graph()
    for node in multigraph.nodes_iter():
        G.add_node(node)
    for edge in multigraph.edges_iter():
        for existing_edge in G.edges_iter():
            if existing_edge[0] == edge[0] and existing_edge[1] == edge[1]:
                G.edge[edge[0]][edge[1]]['weight'] += 1
        G.add_edge(edge[0], edge[1], weight=1)
    return G
#     clusters = clustering(G)
#     return clusters

def get_group_size(communities, community_count):
    group_count = []
    for i in range(0, community_count + 1):
        group_count.append(0)
    for i in communities:
        group_count[communities[i]] += 1
    return group_count


def get_number_of_communities(communities):
    community_count = 0
    for i in communities:
        if communities[i] > community_count:
            community_count = communities[i]
    return community_count


def filter_group_by_size(communities, community_count, group_count, min_size):
    groups = [-1]
    for i in range(0, community_count + 1):
        if group_count[i] > min_size:
            groups.append(i)
    for i in communities:
        if communities[i] not in groups:
            communities[i] = -1
    return groups


def add_clustering_communities(infile, outfile):
    json_data = json.load(open(infile))
    multigraph = json_graph.node_link_graph(json_data)
    graph = make_nonmultigraph(multigraph)
    communities = best_partition(graph)
    community_count = get_number_of_communities(communities)
    group_count = get_group_size(communities, community_count)
    groups = filter_group_by_size(communities, community_count, group_count, 9)
    for node in json_data['nodes']:
        c = 1
        node['group'] = 0
        for group in groups:
            if group == communities[node['id']]:
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

add_clustering_communities("/home/arin/thesis/DAC_network_analysis/static/json/old_json/authors_without_groups.json","/home/arin/Desktop/blah.json")
# check_groups("/home/arin/thesis/DAC_network_analysis/static/json/authors.json")