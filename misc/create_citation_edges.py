__author__ = 'arin'
import csv

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.local_settings')

from network_visualizer.models import Papers

def create_csv():
    reader = csv.reader(open('ReferencesList.txt'))
    outfile = open('citation_network_edges.csv', 'w')
    for line in reader:
        if len(line) != 1:
            print line
            source_doi = line[0]
            for index in range(1, len(line)):
                target_doi = line[index]
                outfile.write('{source},{target}\n'.format(source=source_doi, target=target_doi))
def check_links():
    reader = csv.reader(open('list_of_refs.txt'))
    outfile = open('edges.csv', 'w')
    c= 0
    for line in reader:
        source_title = line[0]
        print c
        c+=1
        for index in range (1,len(line)):
            try:
                target = Papers.objects.get(title=line[index])
                source = Papers.objects.get(title = source_title)
                outfile.write('{source},{target}\n'.format(source=source.doi, target=target.doi))
            except Papers.DoesNotExist:
                pass

check_links()