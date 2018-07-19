# -*- coding: utf-8 -*-

# Scrapy settings for geekbench project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'geekbench'

SPIDER_MODULES = ['geekbench.spiders']
NEWSPIDER_MODULE = 'geekbench.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1.2

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'geekbench.pipelines.GeekbenchPipeline': 300,
}

DOWNLOADER_MIDDLEWARES = {
    'geekbench.middlewares.GeekbenchSpiderMiddleware': 400
}

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings

# Wanted to explicitly set this to False as the per page date is changing
# all the time so caching is counter-productive.

HTTPCACHE_ENABLED = False

# The file is saved as JSON using static name. It is processed elsewhere in the code.
FEED_FORMAT = 'json'
FEED_URI = 'file:geekbench.json'

# Feel free to tune wherever you want. This provides enough data to see
# how execution goes without messing the screen completely up.
LOG_LEVEL = 'INFO'
