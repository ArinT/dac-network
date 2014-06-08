__author__ = 'arin'
import json
import os
from django.db import connection
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.local_settings')
def add_urls_to_papers(filename):

    papers = json.load(open(filename))
    cursor = connection.cursor()
    cursor.execute('ALTER TABLE Papers ADD url VARCHAR(300)')
    cursor.close()
    for paper in papers:
        cursor = connection.cursor()
        cursor.execute('UPDATE Papers SET url = %s WHERE DOI = %s',[paper['url'].encode('UTF-8'),paper['doi'].encode('UTF-8')])
        cursor.close()
def remove_url():
    cursor = connection.cursor()
    cursor.execute('ALTER TABLE Papers DROP url')
    cursor.close()

# add_urls_to_papers("papers.json")
remove_url()