__author__ = 'arin'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
import csv
from pprint import pprint
from django.db import connection
def query_degree_frequency_data():
    """A query which returns the number of papers publish in each year by each author and groups by the number of papers.
    This gives a more general concept of how authors publish papers"""
    cursor = connection.cursor()
    cursor.execute(
        'SELECT pubs.ppy as Degree, pubs.yr as Year, COUNT(*) as Frequency FROM ( '
	        'SELECT COUNT(*) as ppy, a.AuthorName as an, a.AuthorID as aid, p.Year as yr FROM Authors a '
		    'JOIN Works w ON w.AuthorID = a.AuthorID '
		    'JOIN Papers p on p.PaperID = w.PaperID '
		    'GROUP BY p.Year, a.AuthorName, a.AuthorID '
		    'ORDER BY p.Year, COUNT(*) DESC ) pubs '
	    'GROUP BY pubs.ppy, pubs.yr '
	    'ORDER BY pubs.yr, pubs.ppy; '
        )
    return cursor.fetchall()
def generate_plot_csv():
    """Generates/formats the data and writes to a csv"""
    results = query_degree_frequency_data()
    min_year = min(results, key = lambda r: r[1])[1]
    max_year = max(results, key = lambda r: r[1])[1]
    max_deg = max(results, key = lambda r: r[0])[0]
    x = [[0 for i in range(max_year - min_year + 1)] for j in range(max_deg)]
    for item in results:
        deg =item[0]
        year = item[1]
        freq = item[2]
        i = deg-1
        j = int(year) - 2002
        x[i][j] = int(freq)
    with open("static/csv/degree_frequency_plot.csv", "w") as writer:
        i = 1
        writer.write("degree")
        for n in range(min_year, max_year + 1):
            writer.write("," + str(n))
        writer.write("\n")
        for row in x:
            writer.write(str(i))
            i+=1
            for column in row:
                writer.write(","+str(column))
            writer.write("\n")
generate_plot_csv()