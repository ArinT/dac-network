__author__ = 'arin'
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')

from network_visualizer.models import Papers
with open('papers.csv','w') as outfile:
    for paper in Papers.objects.all():
        outfile.write('{id},{title},{doi}\n'.format(id=paper.paperid, title= paper.title, doi = paper.doi))