import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'DAC_network_analysis.settings')
from django.test import TestCase
from network_visualizer.query_database import *

# Create your tests here.
class TestQuery(TestCase):
    def test_query_affiliates(self):
        affiliates = get_author_affiliates(463)
        assert(len(affiliates)!= 0)
    def test_query_credits(self):
        credits= get_author_credits(463)
        assert(len(credits)!=0)
    def test_query_author_info(self):
        info = get_author_info(463)
        assert(len(info['credits'])!= 0)
        assert(len(info['affiliates'])!= 0)
    def test_query_paper_info(self):
        info = get_paper_info(53)
        print info