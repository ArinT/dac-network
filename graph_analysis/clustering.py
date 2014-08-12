__author__ = 'arin'
import json
from networkx.algorithms.cluster import clustering
from networkx.algorithms.community import k_clique_communities
from networkx.readwrite import  json_graph
from networkx.classes.graph import Graph
from community import best_partition
from community import partition_at_level
def make_nonmultigraph(multigraph):
    """
        Removes duplicate edges. Instead of having multiple edges going from the same source to the same target,
        this function adds one edge with a weight attribute,
        Parameters:
            multigraph: The multi-graph with multi-edges
        Return:
            G: A new graph which is equivalent to the multi-graph.
    """
    G = Graph()
    for node in multigraph.nodes_iter():
        G.add_node(node)
    for edge in multigraph.edges_iter():
        for existing_edge in G.edges_iter():
            if existing_edge[0] == edge[0] and existing_edge[1] == edge[1]: #If the edge is already in the existing edge list...
                G.edge[edge[0]][edge[1]]['weight'] += 1 # the existing edge's weight is incremented
        G.add_edge(edge[0], edge[1], weight=1)
    return G

def get_group_size(communities, community_count):
    """Counts the number of nodes in each cluster
        Parameters:
            communities: The clustering returned by the community detection algorithm
            community_count: The total number of communities in the clustering
        Return:
            group_count: A list of integers represents how many nodes are in each clustering group
    """

    group_count = []
    for i in range(0, community_count + 1):
        group_count.append(0)
    for i in communities:
        group_count[communities[i]] += 1
    return group_count


def get_number_of_communities(communities):
    """Gets the total number of groups in the clusterings"""
    community_count = 0
    for i in communities:
        if communities[i] > community_count:
            community_count = communities[i]
    return community_count


def filter_group_by_size(communities, community_count, group_count, min_size):
    """ Determines which groups are large enough to be included in the visualization
        If a node is a member of a group which is too small, it is re-assigned to group "-1".
        Parameters:
            communities: The clustering returned by the community detection algorithm
            community_count: The total number of communities in the clustering
            group_count: A list of integers represents how many nodes are in each clustering group
            min_size: The minimum group size to be included
        returns:
            groups: The ids of the groups which should be included
    """
    groups = [-1]
    for i in range(0, community_count + 1):
        if group_count[i] > min_size:
            groups.append(i)
    for i in communities:
        if communities[i] not in groups:
            communities[i] = -1
    return groups

def add_clustering_communities(json_data):
    multigraph = json_graph.node_link_graph(json_data)
    graph = make_nonmultigraph(multigraph)
    communities = best_partition(graph)
    community_count = get_number_of_communities(communities)
    group_count = get_group_size(communities, community_count)
    groups = filter_group_by_size(communities, community_count, group_count, 9)
    #Assigns groups to nodes in the json
    for node in json_data['nodes']:
        c = 1
        node['group'] = 0
        for group in groups:
            if group == communities[node['id']]:
                node['group'] = c
            c+=1
    return json_data