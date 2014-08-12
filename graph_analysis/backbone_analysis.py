__author__ = 'arin'
import json

def write_to_json(outfile, j):
    """ Creates a new json file and writes the input json to the file.
        Parameters:
            outfile: File to write to.
            j: json serializable object
    """
    writer = open(outfile, "w+")
    writer.write(json.dumps(j))


def construct_backbone_json(json_data, alpha):
    """
        Filters out nodes which do not have a betweenness centrality greater
        than alpha. Writes a boolean value to the json object parameter
        specifying whether the element belongs to the backbone or not.
        Parameters:
            json_data: a json object containing the graph data.
            alpha: the threshold to filter by
        Returns:
            The modified json_data parameter.
    """
    for node in json_data['nodes']:
        if node['betweennessCentrality'] > alpha and node['group']!=1:
            node['backbone'] = True
        else:
            node['backbone'] = False
    return json_data


def add_network_backbone(infile, outfile, alpha):
    """Loads json from IO, does analysis and writes back."""
    json_data = json.load(open(infile))
    backbone_json = construct_backbone_json(json_data, alpha)
    write_to_json(outfile, backbone_json)


def main():
    """Does analysis for both citation and author network"""
    add_network_backbone("/home/arin/thesis/DAC_network_analysis/static/json/authors.json",
                                "/home/arin/thesis/DAC_network_analysis/static/json/authors.json", .05)
    add_network_backbone("/home/arin/thesis/DAC_network_analysis/static/json/citations.json",
                                "/home/arin/thesis/DAC_network_analysis/static/json/citations.json", .1)


main()