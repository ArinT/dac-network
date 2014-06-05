__author__ = 'arin'
import unittest
from crawler.scopus_crawler_sel import extractReferences
class TestCrawler(unittest.TestCase):
    def test_extract_refs(self):
        refs = extractReferences("On Performance Enhancement of Parallel Kinematic Machine")
        print refs
        assert(len(refs)!=0)
    def test_odd_cases(self):
        refs = extractReferences("Improved Disassembly Matrices for Disassembly Processes")
        print refs
        assert(len(refs)!=0)