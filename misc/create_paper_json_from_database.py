__author__ = 'arin'
import json
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
from network_visualizer.models import Papers
def generate_paper_json(outfile):
    """Creates a json file from the Paper table in the database.
    This file is used to for creating the citation network"""
    writer = open(outfile,"w+")
    papers = Papers.objects.all()
    json_papers = []

    for paper in papers:
        json_paper = {}
        json_paper['paperid'] = paper.paperid
        json_paper['title'] = paper.title
        json_paper['doi'] = paper.doi
        json_paper['numauthors'] = paper.numauthors
        json_paper['url'] = paper.url
        json_papers.append(json_paper)
    writer.write(json.dumps(json_papers))
generate_paper_json('/home/arin/thesis/DAC_network_analysis/misc/papers.json')