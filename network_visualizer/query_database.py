__author__ = 'arin'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')

from network_visualizer.models import Papers
from django.db import connection


def get_author_credits(author_id):
    cursor = connection.cursor()
    cursor.execute('SELECT title, url FROM Papers '
                   'JOIN Works ON Works.PaperId = Papers.PaperID '
                   'JOIN Authors ON Authors.AuthorID = Works.AuthorId '
                   'WHERE Authors.AuthorID = %s;', [author_id])
    res = cursor.fetchall()
    credits = []
    for item in res:
        credits.append({'title': item[0].encode('utf-8'), 'url': item[1].encode('utf-8')})
    return credits

def get_author_affiliates(author_id):
    cursor = connection.cursor()
    cursor.execute('SELECT a.authorName, COUNT(*) FROM Works w1 '
                   'JOIN Works w2 on w1.paperId = w2.paperId '
                   'JOIN Authors a on w2.authorId = a.AuthorId '
                   'WHERE w2.authorId <> w1.authorId AND '
                   'w1.authorId = %s '
                   'GROUP BY w1.authorId, w2.authorId, a.authorName '
                   'ORDER BY COUNT(*) DESC; ',[author_id])
    res = cursor.fetchall()
    affiliates = []
    for item in res:
        affiliates.append({'name':item[0].encode('UTF-8'),'count':int(item[1])})
    return affiliates

def get_author_info(author_id):
    credits = get_author_credits(author_id)
    affiliates = get_author_affiliates(author_id)
    info = {'credits':credits,'affiliates':affiliates}
    return info

def get_similar_papers(paper_id):
    cursor = connection.cursor()
    cursor.execute('SELECT p2.title, p2.url  FROM Papers p1 '
                   'JOIN TopFives tf ON tf.parentId = p1.PaperID '
                   'JOIN Papers p2 ON p2.PaperID = tf.childId '
                   'WHERE p1.PaperID = %s '
                   'ORDER BY tf.rank;', [paper_id])
    res = cursor.fetchall()
    results = []
    for item in res:
        results.append({'title': item[0].encode('utf-8'), 'url': item[1].encode('utf-8')})
    return results

def get_citations(paper_id):
    cursor = connection.cursor()
    cursor.execute('SELECT p.title, p.url FROM Citations c '
                   'JOIN Papers p on p.paperId = c.targetPaperId '
                   'WHERE c.sourcePaperId = %s; ',[paper_id])
    res = cursor.fetchall()
    cites = []
    for item in res:
        cites.append({'name':item[0].encode('utf-8'), 'url':item[1].encode('utf-8')})
    return cites
def get_cited_by(paper_id):
    cursor = connection.cursor()
    cursor.execute('SELECT p.title, p.url, p.doi FROM Citations c '
                   'JOIN Papers p on p.paperId = c.sourcePaperId '
                   'WHERE c.targetPaperId = %s; ',[paper_id])
    res = cursor.fetchall()
    cited = []
    for item in res:
        cited.append({'name':item[0].encode('UTF-8'), 'url':item[1].encode('UTF-8'), 'doi':item[2]})
    return cited
def get_paper_authors(paper_id):
    cursor = connection.cursor()
    cursor.execute('SELECT a.authorName, a.authorId FROM Works w '
                   'JOIN Authors a on a.authorId = w.AuthorId '
                   'WHERE w.paperId = %s; ', [paper_id])
    res = cursor.fetchall()
    authors = []
    for item in res:
        authors.append({'name':item[0].encode('UTF-8'),'id':int(item[1])})
    return authors
def get_paper_info(paper_id):
    similar_papers = get_similar_papers(paper_id)
    cites = get_citations(paper_id)
    cited = get_cited_by(paper_id)
    authors = get_paper_authors(paper_id)
    info = {'similar_papers':similar_papers,'cites':cites,'cited':cited,'authors':authors}
    return info