#!/usr/bin/env python
from bs4 import BeautifulSoup
from unidecode import unidecode
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
from network_visualizer.models import Papers, Works, Authors

# TODO: change this line to the relevant file to parse
f = open("misc/2014vol2.html", "r")
content = f.read()
soup = BeautifulSoup(content, "html.parser")
articles = soup.find_all(class_="contentTocArticle")

# Get latest IDs because for some reason Papers and Works aren't autoincrementing
paper_id = Papers.objects.latest("paperid").paperid + 1
author_id = Authors.objects.latest("authorid").authorid + 1


for article in articles:
    title = article.find(class_="articleTitle").get_text().strip()
    # Conference proceeding entries look like articles but don't have an articleauthors field
    try:
        authors = article.find(class_="articleAuthors").find_all("a")
    except AttributeError:
        continue
    authors_sql = []
    for author in authors:
        # Sometimes names are accented, we avoid that by converting to unidecode
        author_string = unidecode(author.string)
        try:
            author_sql = Authors.objects.get(authorname=author_string)
        except Authors.DoesNotExist:
            author_sql = Authors.objects.create(authorname=author_string, authorid=author_id)
            author_id += 1
            author_sql.save()
        authors_sql.append(author_sql)
    doi = article.find(class_="articleCitation").get_text().strip().split()[0]
    paper = Papers.objects.create(paperid=paper_id, title=title, doi=doi, numauthors=len(authors_sql))
    paper_id += 1
    paper.save()
    for author in authors_sql:
        work = Works.objects.create(authorid=author.authorid, paperid=paper.paperid)
        work.save()
