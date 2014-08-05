__author__ = 'arin'

from networkx.readwrite import json_graph
import networkx as nx
import json
from graph_analysis.clustering import  make_nonmultigraph

def write_to_json(outfile, j):
    writer = open(outfile, "w+")
    writer.write(json.dumps(j))


def construct_backbone_json(json_data, alpha):
    for node in json_data['nodes']:
        if node['betweennessCentrality'] > alpha and node['group']!=1:
            node['backbone'] = True
        else:
            node['backbone'] = False
    return json_data


def add_network_backbone(infile, outfile, alpha):
    json_data = json.load(open(infile))
    backbone_json = construct_backbone_json(json_data, alpha)
    write_to_json(outfile, backbone_json)


def main():
    add_network_backbone("/home/arin/thesis/DAC_network_analysis/static/json/authors.json",
                                "/home/arin/thesis/DAC_network_analysis/static/json/authors.json", .05)
    add_network_backbone("/home/arin/thesis/DAC_network_analysis/static/json/citations.json",
                                "/home/arin/thesis/DAC_network_analysis/static/json/citations.json", .1)


main()