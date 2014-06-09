__author__ = 'arin'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')

from network_visualizer.models import Papers
from django.db import connection
def get_author_info(author_id):
    cursor = connection.cursor()
    cursor.execute('SELECT title, url FROM Papers '
                   'JOIN Works ON Works.PaperId = Papers.PaperID '
                   'JOIN Authors ON Authors.AuthorID = Works.AuthorId '
                   'WHERE Authors.AuthorID = %s;',[author_id])
    res = cursor.fetchall()
    results = []
    for item in res:
        results.append({'title':item[0],'url':item[1]})
    return results
def get_paper_info(paper_id):
    cursor = connection.cursor()
    cursor.execute('SELECT p2.title, p2.url  FROM Papers p1 '
                   'JOIN TopFives tf ON tf.parentId = p1.PaperID '
                   'JOIN Papers p2 ON p2.PaperID = tf.childId '
                   'WHERE p1.PaperID = %s '
                   'ORDER BY tf.rank;',[paper_id])

    res = cursor.fetchall()
    results = []
    for item in res:
        results.append({'title':item[0],'url':item[1]})
    return results
from pprint import pprint
pprint(get_author_info(463))
pprint(get_paper_info(463))