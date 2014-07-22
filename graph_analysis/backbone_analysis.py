__author__ = 'arin'
# Serrano, Boguna, Vespigani backbone extractor
# from http://www.pnas.org/content/106/16/6483.abstract
# Thanks to Michael Conover and Qian Zhang at Indiana with help on earlier versions
# Thanks to Clay Davis for pointing out an error

from networkx.readwrite import json_graph
import networkx as nx
import json
from graph_analysis.clustering import  make_nonmultigraph
def extract_backbone(g, alpha):
  backbone_graph = nx.Graph()
  for node in g:
      number_of_nodes = len(g[node])
      if number_of_nodes > 1:
          total_weight = sum( g[node][neighbor]['weight'] for neighbor in g[node] )
          for neighbor in g[node]:
              edgeWeight = g[node][neighbor]['weight']
              pij = float(edgeWeight)/total_weight
              if (1-pij)**(number_of_nodes-1) < alpha: # equation 2
                  backbone_graph.add_edge( node,neighbor, weight = edgeWeight)
  return backbone_graph
def write_to_json(outfile, j):
    writer = open(outfile, "w+")
    writer.write(json.dumps(j))


def reconstruct_backbone_json(bg, json_data):
    backbone_ids = [x for x in bg.node]
    backbone_nodes = []
    backbone_edges = []
    for node in json_data['nodes']:
        if node['id'] in backbone_ids:
            backbone_nodes.append(node)
    for edge in json_data['links']:
        if edge['source'] in backbone_ids and edge['target'] in backbone_ids:
            src = -1
            tgt = -1
            for i, x in enumerate(backbone_nodes):
                if x['id'] == edge['source']:
                    src = i
                if x['id'] == edge['target']:
                    tgt = i
            backbone_edges.append({'source': src, 'target': tgt})
    j = {'nodes': backbone_nodes, 'links': backbone_edges}
    return j


def main():
    json_data = json.load(open("/home/arin/thesis/DAC_network_analysis/static/json/authors.json"))
    muligraph = json_graph.node_link_graph(json_data)
    graph = make_nonmultigraph(muligraph)
    bg = extract_backbone(graph, 0.375)
    backbone_json = reconstruct_backbone_json(bg, json_data)
    write_to_json("/home/arin/thesis/DAC_network_analysis/static/json/authors_backbone.json", backbone_json)
main()