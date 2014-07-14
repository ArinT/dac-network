__author__ = 'arin'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
import csv
from django.db import connection
def generate_chronological_visualization():
    cursor = connection.cursor()
    cursor.execute(
        'SELECT COUNT(*) as "Publications per year", a.AuthorName as "Author Name", a.AuthorID as "Author ID", SUBSTRING(p.DOI,5,4) as "Year" FROM Authors a '
	        'JOIN Works w ON w.AuthorID = a.AuthorID '
	        'JOIN Papers p on p.PaperID = w.PaperID '
            'WHERE a.AuthorID IN '
                '(SELECT ab.AuthorID from (SELECT a1.AuthorID FROM Authors a1 '
                'JOIN  Works w2 ON w2.AuthorID = a1.AuthorID '
                'GROUP BY a1.AuthorID '
                'ORDER BY COUNT(*) DESC '
                ') ab) '
	        'GROUP BY SUBSTRING(p.DOI,3,7), a.AuthorName, a.AuthorID '
	        'ORDER BY a.AuthorName, SUBSTRING(p.DOI,5,4), COUNT(*) DESC ')
    return cursor.fetchall()
def write_to_json():
    writer = open("../static/csv/chronological_publications.csv", "w+")
    results = generate_chronological_visualization()
    for tuple in results:
        writer.write("{},{},{} \n".format(tuple[1],float(tuple[0]),tuple[3]))
def create_array(filename):
    names = set()
    dates = ["2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012"]
    f = open(filename)
    reader = csv.reader(f)
    for line in reader:
        names.add(line[0])
    writer = open("../static/csv/chronological_array.csv","w+")

    for name in names:
        for date in dates:
            found = False
            f.seek(0)
            for line in reader:
                if line[0] == name and line[2].strip() ==date:
                    writer.write("{},{},{}\n".format(name,line[1],date))
                    found = True
            if not found:
                writer.write("{},0,{}\n".format(name,date))
write_to_json()
create_array("../static/csv/chronological_publications.csv")