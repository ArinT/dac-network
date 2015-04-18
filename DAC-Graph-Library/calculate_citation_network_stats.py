# from graph_analysis.clustering import add_clustering_communities
# from graph_analysis.calculate_centrality import calculate_all_centralities
import json


from networkx.readwrite import json_graph
from networkx.algorithms import centrality
from networkx.classes.digraph import DiGraph
from networkx.exception import NetworkXError

def calculate_all_centralities(data):
    """
        Calculates all four centralities metrics for the input graph
        Paramaters:
            data: a json object which represents the graph.
            This json is manipulated and the necessary metrics are added to it.
    """
    G = json_graph.node_link_graph(data) #loads the data to a NetworkX graph object
    #Calculates three of the metrics
    degree = centrality.degree_centrality(G)
    closeness = centrality.closeness_centrality(G)
    betweeness = centrality.betweenness_centrality(G)
    eigenvector_fail = False
    try: #Eigenvector centrality can fail to converge.
        eigenvector = centrality.eigenvector_centrality(DiGraph(G),max_iter=100000)
    except NetworkXError: #Eigenvector values will be None if calculation fails.
        eigenvector = []
        eigenvector_fail = True
        print "Max iterations exceeded"
    degree_max = -1.0
    closeness_max = -1.0
    betweeness_max = -1.0
    eigenvector_max = -1.0
    for author in data['nodes']: #Adds the unnormalized values in the json
        i = author['id']
        author['degreeCentralityUnnormalized'] = degree[i]
        author['closenessCentralityUnnormalized'] = closeness[i]
        author['betweennessCentralityUnnormalized'] = betweeness[i]
        author['eigenvectorCentralityUnnormalized'] = eigenvector[i] if not eigenvector_fail else 1.0

    #Finds the highest values for each centrality type
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

    #Normalizes the values
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

    #Adds the normalized values to the json
    for author in data['nodes']:
        i = author['id']
        author['degreeCentrality'] = degree[i]
        author['closenessCentrality'] = closeness[i]
        author['betweennessCentrality'] = betweeness[i]
        author['eigenvectorCentrality'] = eigenvector[i] if not eigenvector_fail else 1.0
    return data

def write_json_to_file(outfile, j):
    writer = open(outfile,'w+')
    writer.write(json.dumps(j))

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
# generate  = [generate_author_network_json,generate_citation_network_json]
# author_network_json = generate[type](year)
# print ("Author" if type == 0 else "Citation")+" Network generated for "+str(year)

# json_data = open('../static/json/authors.json')
outfile = "citation_central_test.json"
json_data = open('citations_test.json')
author_network_json = json.load(json_data)
author_network_json_with_centrality = calculate_all_centralities(author_network_json)
# print ("Author" if type == 0 else "Citation")+" Network centrality calculated for "+str(year)
complete_author_network_json = add_clustering_communities(author_network_json_with_centrality)
# print ("Author" if type == 0 else "Citation")+" Network community clustering calculated for "+str(year)
write_json_to_file(outfile, complete_author_network_json)
print "done"
# print "Complete "+("Author" if type == 0 else "Citation")+" Network written to "+outfile