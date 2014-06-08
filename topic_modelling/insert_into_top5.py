__author__ = 'arin'
import csv
import os
from django.db import connection
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.local_settings')
def insert_csv(filename):
        reader = csv.reader(open(filename))
        cursor = connection.cursor()
        cursor.execute(
            'DROP TABLE IF EXISTS TopFives;'
            'CREATE TABLE TopFives(parentId INT, childId INT, rank INT);'
        )
        cursor.close()
        i = 0

        for line in reader:
            print i
            i+=1
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO TopFives (parentId, childId, rank) VALUES '
                '('
                '(SELECT PaperId FROM Papers WHERE DOI = %s),'
                '(SELECT PaperId FROM Papers WHERE DOI = %s),'
                '%s );',[line[0].encode('UTF-8'),line[1].encode('UTF-8'),line[2].encode('UTF-8')])
            cursor.close()

insert_csv('top5.csv')
