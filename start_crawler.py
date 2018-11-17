import os
import sys
import shutil
import datetime
import argparse
import logging

import pandas as pd

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from geekbench.spiders.geekbench import GeekbenchSpider


def convert_data(json_file: str, hfs_prefix: str) -> str:
    """ Converts JSON into Pandas DataFrame and then into hfs compressed file to save data"""
    hfs_file_name = None

    if os.path.exists(json_file):
        # Loading json into DataFrame. This will already reveal issues in data if there are any
        df_new_data = pd.read_json(json_file, orient='columns')

        # This helps to ensure that time-format will work later
        df_new_data['Upload Date'] = pd.to_datetime(df_new_data['Upload Date'])

        # Dropping unnecessary data. This information doesn't change inside the same chipset
        # so storing as part of every sample is kind of redudant. Comment the code if you want to keep them
        df_new_data.drop(['L1 Data Cache', 'L1 Instruction Cache', 'L2 Cache', 'L3 Cache'], inplace=True, axis=1, errors='ignore')

        # Each hfs file is specific to the scraping session so timestamp in the file name
        # works perfectly for this purpose.
        date_appendix = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')

        hfs_file_name = f'{hfs_prefix}_{date_appendix}.h5'

        df_new_data.to_hdf(hfs_file_name, 'df', complevel=9, complib='blosc:zstd')

        # JSON file is removed after processing
        os.remove(json_file)

    return hfs_file_name


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Start Geekbench crawling process.")
    parser.add_argument('-p', '--path',
                        help="path for the destination file directory. Default '.'",
                        default='.'
                        )
    parser.add_argument('-d', '--debug',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="Debug level used with scraping. Use Python level eg. INFO, DEBUG, ...",
                        )

    parser.add_argument('-j', '--json',
                        help='Perform only json converion without any scraping. '
                        )

    args = parser.parse_args()

    hfs_file_prefix = 'geekbench_data'

    # JSON choice is used to overcome the situations when JSON file has been created
    # but, for some reason, parts of the script was broken and the conversion didn't happen
    if not args.json:
        # Path must be directory and exists
        if not os.path.isdir(args.path):
            print(f"Provided directory {args.path} doesn't exists")
            sys.exit(0)

        json_file = 'geekbench.json'

        settings = get_project_settings()

        if args.debug:
            # Maps debugging levels string into logging.XXX variable
            logging_val = {'LOG_LEVEL' : getattr(logging, args.debug)}
            settings.update(logging_val)
            print('logging variable set')

        process = CrawlerProcess(settings)

        process.crawl(GeekbenchSpider)
        process.start()

    else:
        # Checking if the file exists to provide sensible error notice.
        if not os.path.exists(args.json):
            print(f"Specified JSON file {args.json} doesn't exists!")
            sys.exit(0)

        json_file = args.json

    hfs5_file = convert_data(json_file, hfs_file_prefix)

    if hfs5_file:
        shutil.move(hfs5_file, args.path)
    else:
        print("Hfs5 file creation failed! Please, use JSON file")




