__author__ = 'arin'
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
import csv
from unidecode import unidecode
from django.db import connection
def generate_chronological_visualization():
    """A query which returns a set of tuples indicating the number of papers that each author
    has published in each year"""
    cursor = connection.cursor()
    cursor.execute(
        'SELECT COUNT(*) as "Publications per year", a.AuthorName as "Author Name", a.AuthorID as "Author ID", p.Year as "Year" FROM Authors a '
	        'JOIN Works w ON w.AuthorID = a.AuthorID '
	        'JOIN Papers p on p.PaperID = w.PaperID '
            'WHERE a.AuthorID IN '
                '(SELECT ab.AuthorID from (SELECT a1.AuthorID FROM Authors a1 '
                'JOIN  Works w2 ON w2.AuthorID = a1.AuthorID '
                'GROUP BY a1.AuthorID '
                'ORDER BY COUNT(*) DESC '
                ') ab) '
	        'GROUP BY p.Year, a.AuthorName, a.AuthorID '
	        'ORDER BY a.AuthorName, p.Year, COUNT(*) DESC ;')
    return cursor.fetchall()
def generate_chronological_visualization_top100():
    """A query which returns a set of tuples indicating the number of papers that each author
    has published in each year. Only authors who are in the top 100 contributors overall are included"""
    cursor = connection.cursor()
    cursor.execute(
        'SELECT COUNT(*) as "Publications per year", a.AuthorName as "Author Name", a.AuthorID as "Author ID", p.Year as "Year" FROM Authors a '
	        'JOIN Works w ON w.AuthorID = a.AuthorID '
	        'JOIN Papers p on p.PaperID = w.PaperID '
            'WHERE a.AuthorID IN '
                '(SELECT ab.AuthorID from (SELECT a1.AuthorID FROM Authors a1 '
                'JOIN  Works w2 ON w2.AuthorID = a1.AuthorID '
                'GROUP BY a1.AuthorID '
                'ORDER BY COUNT(*) DESC '
                'LIMIT 100) ab) '
	        'GROUP BY p.Year, a.AuthorName, a.AuthorID '
	        'ORDER BY a.AuthorName, p.Year, COUNT(*) DESC ;')
    return cursor.fetchall()
def generate_chronological_visualization_yearly(year):
    """A query which returns a set of tuples indicating the number of papers that each author
    has published in each year. Only authors who are in the top 50 contributors for the given year are included"""
    cursor = connection.cursor()
    cursor.execute(
        'SELECT COUNT(*) as "Publications per year", a.AuthorName as "Author Name", a.AuthorID as "Author ID", p.Year as "Year" FROM Authors a '
            'JOIN Works w ON w.AuthorID = a.AuthorID '
            'JOIN Papers p on p.PaperID = w.PaperID '
            'WHERE a.AuthorID IN '
                '(SELECT ab.AuthorID from (SELECT a1.AuthorID, COUNT(*) FROM Authors a1 '
                    'JOIN  Works w2 ON w2.AuthorID = a1.AuthorID '
                    'JOIN  Papers p1 on p1.PaperId = w2.PaperId '
                    'WHERE p1.Year = %s '
                    'GROUP BY a1.AuthorID '
                    'ORDER BY COUNT(*) DESC '
                    'LIMIT 50) ab) '
            'GROUP BY p.Year, a.AuthorName, a.AuthorID '
            'ORDER BY a.AuthorName, p.Year, COUNT(*) DESC ;', [str(year)])
    return cursor.fetchall()
def write_to_json(outfile):
    with open(outfile, "w+") as writer:
        results = generate_chronological_visualization()
        for tuple in results:
            writer.write("{},{},{} \n".format(unidecode(tuple[1]),float(tuple[0]),tuple[3]))
def write_to_json_top100(outfile):
    with open(outfile, "w+") as writer:
        results = generate_chronological_visualization_top100()
        for tuple in results:
            writer.write("{},{},{} \n".format(unidecode(tuple[1]),float(tuple[0]),tuple[3]))
def write_to_json_yearly(outfile, year):
    with open(outfile, "w+") as writer:
        results = generate_chronological_visualization_yearly(year)
        for tuple in results:
            writer.write("{},{},{} \n".format(unidecode(tuple[1]),float(tuple[0]),tuple[3]))
def create_array(infile, outfile):
    """In order to be read into the streamgraph, the tuples must be formatted similar to a 2d array
        In an N x N array, the first N elements would pertain to the first column, the second N to the second...
        This function handles formating the tuples properly and writing to a .csv to be read by the d3 code"""
    names = set()
    dates = ["2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014"]
    f = open(infile)
    reader = csv.reader(f)
    for line in reader:
        names.add(line[0])
    writer = open(outfile,"w+")
    writer.write("key,value,date\n")
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
for i in range(13):
    write_to_json_yearly("static/csv/yearly_csvs/chronological_publications_"+str(2002+i)+".csv", 2002+i)
    create_array("static/csv/yearly_csvs/chronological_publications_"+str(2002+i)+".csv",
                 "static/csv/yearly_csvs/chronological_array_"+str(2002+i)+".csv")
write_to_json("static/csv/chronological_publications.csv")
create_array("static/csv/chronological_publications.csv",
    "static/csv/chronological_array.csv")