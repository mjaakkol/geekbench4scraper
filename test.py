#!/usr/bin/python
import unittest
import os
import json

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from geekbench.spiders.geekbench import GeekbenchSpider

json_file = 'geekbench.json'

class TestGeekbench(unittest.TestCase):
    """
    System test class for Geekbench scraper

    """

    @classmethod
    def setUpClass(cls):
        """
        Performs limited scraping pass and loads the results
        for further analysis
        """

        # Removing the old file if there is one
        if os.path.exists(json_file):
            os.remove(json_file)

        # Starting crawling process
        process = CrawlerProcess(settings=get_project_settings())

        assert(process)

        process.crawl(GeekbenchSpider, n_pages=1)
        process.start()

    def test_is_file_existing(self):
        self.assertTrue(os.path.exists(json_file), msg="There was no file existing")


    def test_record(self):
        with open(json_file) as data:
            d = json.load(data)

            self.assertTrue(len(d), msg="json file is empty")

            for i, entry in enumerate(d):
                with self.subTest(i=i):
                    self.assertTrue(entry['version'])
                    self.assertTrue(entry['Single-Core Score'])
                    self.assertTrue(entry['Multi-Core Score'])
                    self.assertTrue(entry['multi_Memory Score'])
                    self.assertTrue(type(entry['Motherboard'] == str))

            return None

        self.assertTrue(False, msg="No JSON file found")

if __name__ == '__main__':
    unittest.main()