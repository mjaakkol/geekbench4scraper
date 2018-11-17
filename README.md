**Geekbench Android Benchmark Results Web-Scraper**

Have ever wondered how those leaked smartphones are found from Geekbench? (hint: not by manually going through thousand pages of results)

This is Android Geekbench 4 result web-scraper using [Scrapy](https://scrapy.org/). The scaper can be invoked using command **_scrapy crawl geekbench_** when wanting to use directly through Scrapy.

Scraper outputs the results into JSON-file placed at the the root of the scraper. JSON has been made "Pandas-friendly" so you should be able to load it right in.

Extra emphasis has been placed into commenting the code to help somebody else wanting to make their own scraper (eg. expanding beyond smartphones)

Alternative way of starting scraping is through **_python start_crawler.py -p /mydata_store/ -d WARNING_** for providing better controls from the command line as well as getting some data preprocessing. The file is processed through Pandas so you need to have it installed prior using this shortcut. The end result is HFS compressed file.

---

## How to install

Scraper has been developed using Python 3.6 (& 3.7) and Scrapy 1.5 but it should be easy to convert the assets int earlier versions of both if needed (some string operations are using new features introduced in Python 3.6).

Scrapy is the only external dependency and it can be installed through **_pip install scrapy_**.

---


