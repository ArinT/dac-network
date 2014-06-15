__author__ = 'arin'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
import csv
from pprint import pprint
from django.db import connection
def query_degree_frequency_data():
    cursor = connection.cursor()
    cursor.execute(
        'SELECT pubs.ppy as Degree, pubs.yr as Year, COUNT(*) as Frequency FROM ( '
	        'SELECT COUNT(*) as ppy, a.AuthorName as an, a.AuthorID as aid, SUBSTRING(p.DOI,5,4) as yr FROM Authors a '
		    'JOIN Works w ON w.AuthorID = a.AuthorID '
		    'JOIN Papers p on p.PaperID = w.PaperID '
		    'GROUP BY SUBSTRING(p.DOI,3,7), a.AuthorName, a.AuthorID '
		    'ORDER BY SUBSTRING(p.DOI,5,4), COUNT(*) DESC ) pubs '
	    'GROUP BY pubs.ppy, pubs.yr '
	    'ORDER BY pubs.yr, pubs.ppy; '
        )
    return cursor.fetchall()
def generate_plot_csv():
    results = query_degree_frequency_data()
    x = [[0 for i in range(11)] for j in range(9)]
    for item in results:
        deg =item[0]
        year = item[1]
        freq = item[2]
        i = deg-1
        j = int(year) - 2002
        x[i][j] = int(freq)
    writer = open("../static/csv/degree_frequency_plot.csv", "w+")
    i = 1
    for row in x:
        writer.write(str(i))
        i+=1
        for column in row:
            writer.write(","+str(column))
        writer.write("\n")
generate_plot_csv()