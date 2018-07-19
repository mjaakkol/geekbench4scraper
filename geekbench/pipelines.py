# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

# Only leaves digits and '.' in place to make the value numeric
RE_MATCH=re.compile(r'(\d|\.)+')

class GeekbenchPipeline(object):
    """
    Pipeline class to make value specific processing. As the items are 'complete',
    we can rely on all the mandatory fields to be present.
    """
    def process_item(self, item, spider):
        """
        Method handling all item specific processing.

        Returns dictionary containing scraped report.
        """

        # Memory has extra postfix letters and they need to be remove
        # and then converted into actual integer
        numeric = RE_MATCH.match(item['Memory']).group(0)
        item['Memory'] = int(numeric)

        # The same case as above but here the value is a float
        numeric = RE_MATCH.match(item['Base Frequency']).group(0)
        item['Base Frequency'] = float(numeric)

        """
        Some folks identify MB as number making it 'int' in the spider causing
        Pandas to get crazy so the value is explicity marked as 'str'.

        Also sometimes motherboard information is missing but as it is not
        necessarily making the data obsolete, the result is still stored.
        """
        item['Motherboard'] = str(item['Motherboard']) if 'Motherboard' in item else ''

        # In order to keep potential string processing simples, they are all
        # converted into lowercase strings.
        for key in item:
            if type(item[key]) is str:
                item[key] = item[key].lower()

        return item
