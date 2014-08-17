__author__ = 'arin'
import json
from django.db import connection

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
def insert_all_keywords(filename):
    """Creates a list of all keywords and adds them to the database"""
    papers = json.load(open(filename))
    keywords = set()
    for paper in papers:
        for keyword in paper['keywords']:
            keywords.add(keyword.lower().strip())
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Keywords (KeywordId  INT NOT NULL PRIMARY KEY AUTO_INCREMENT, Keyword VARCHAR(50))')
    cursor.close()
    for keyword in keywords:
        cursor= connection.cursor()
        cursor.execute('INSERT INTO Keywords (Keyword) VALUES (%s)', [keyword.encode('UTF-8')])
        cursor.close()
def insert_keywords_for_papers(filename):
    """
        Creates a table which associates papers with the keywords which are associated
        with them
    """
    papers = json.load(open(filename))
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS KeywordToPaper (PaperId  INT, KeywordId INT)')
    cursor.close()
    for paper in papers:
        for keyword in paper['keywords']:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO KeywordToPaper (PaperId, KeywordId) VALUES ('
                           '(SELECT PaperId from Papers WHERE DOI = %s) '
                           ','
                           '(SELECT KeywordId from Keywords WHERE Keyword = %s)'
                           ');',[paper['doi'].encode('UTF-8'),keyword.lower().strip().encode('UTF-8')])
            cursor.close()
insert_keywords_for_papers("papers.json")