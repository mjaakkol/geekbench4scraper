import re
import scrapy

class GeekbenchSpider(scrapy.Spider):
    """
    Geekbench spider for Android devices. The spider spits
    out dictionary objects with scraped fields for further processing in
    the pipeline.

    The spider is tapping in to Geekbench Recent Results page.


    """
    name="geekbench"
    start_url="https://browser.geekbench.com"

    def start_requests(self):
        """
        Default entry point for the spider. Geekbench publishes the last 1000
        results. Hardcoding is not good programming practice but not the worst
        offence in the history of programming in this context.

        Spider also accepts parameter 'n_pages' as command-line argument to
        limit the number of scraped pages to help with testing.

        The method spans a new request to each individual page.

        Yields new Scrapy Requests or None if none if found
        """

        # No need to worry about having n_pages as it comes outside the class
        # through the configuration
        # pylint: disable=E1101
        for index in range(1, 1000 if not hasattr(self, 'n_pages') else int(self.n_pages)+1):
            yield scrapy.Request(url=(self.start_url + f'/v4/cpu?page={index}'))

    def parse(self, response):
        """
        First callback by the framework. This provides as individual pages where
        we can enter into individual result pages.

        Yields new Scrapy Requests or None if none if found
        """
        products = response.css("tr")
        # Dropping the title row from the rest of the rows
        products.pop(0)

        for product in products:
            model =  product.css("td.model span::text").extract_first().replace("\n","")
            platform = product.css("td.platform::text").extract_first().replace("\n","")

            # Spider is only interested of Android results. This is the place to
            # start if somebody wants to modify this for other platforms.
            # The spider accepts both 32- and 64-bit platforms
            if platform.startswith("Android"):
                self.logger.debug("New request for %s %s", model, platform)

                # Hyperlink to the actual product result.
                link = product.css("td.model a::attr(href)").extract_first()

                yield scrapy.Request(url=self.start_url+str(link), callback=self.parse_links)
            else:
                self.logger.debug("Skipped %s %s", model, platform)

    def parse_links(self, response):
        """
        Method for parsing the actual result page. All the results are collected into
        phone_table dictionary object.

        Returns dictionary containing the performance results.
        """
        phone_table = {"version":response.css("tfoot td::text").extract_first(),}

        # The loop iterates through all the tables in the list of tables
        # There are different tables for each major sections
        for table in response.css("div.table-responsive"):
            for tr in table.css('tr'):
                key = tr.css('.name::text').extract_first()

                # If the name is null, we skip it.
                if not key:
                    continue

                key = key.strip(' \n\t\r')

                # Some special magic is needed as some of them are in Chinese.
                if key[0] == '\u5355':
                    # This character stands for single core
                    key = "Single-Core Score"

                elif key[0] == '\u591a':
                    # This character stands for multi core
                    key = "Multi-Core Score"

                # Extracting the raw value.
                value = tr.css('.value::text').extract_first()

                # The ultimate value can either be .value or .score
                if not value:
                    score = tr.css(".score::text").extract()

                    if not score:
                        self.logger.debug("Value was incomprehensible for key %", key)
                        continue

                    # Score is assigned to value as the rest of the processing
                    # is the same
                    value = "".join(score).strip()

                value = value.strip(' \n\t\r')

                # Let's do some little processing while at it. Effectively,
                # the values should be assigned into generics types when possible.
                # More key specific processing is done outside the spider.
                if value.isdigit():
                    value = int(value)
                elif value.isdecimal():
                    value = float(value)

                self.logger.debug('name %s and phone value %s lengths %d',key ,value, len(key))

                # To run everything from the early headers to single- and multi-
                # processor scores, the determination of multi-processing is done
                # at key bases. If the key has already been taken, then this must
                # be multi-processing section.
                if key in phone_table:
                    phone_table["multi_" + key] = value
                else:
                    phone_table[key] = value

        yield phone_table
