from urllib.parse import urljoin
from urllib.parse import urlparse

import scrapy
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor

class SitemapSpider(scrapy.Spider):
    name = "sitemap"
    allowed_domains = ["backmarket.fr"]
    start_urls = ["https://www.backmarket.fr/fr-fr"]

    # allowed_domains = ["elpais.com"]
    # start_urls = ["https://elpais.com/"]

    def __init__(self, *args, **kwargs):
        super(SitemapSpider, self).__init__(*args, **kwargs)

        self.link_extractor = LinkExtractor(
            allow_domains=self.allowed_domains,
            unique=True,
        )

    def parse(self, response: HtmlResponse, **kwargs):
        # for link in response.css("a::attr(href)").getall():
        for link in self.link_extractor.extract_links(response):
            parsed_url = urlparse(link.url)
            absolute_url = urljoin(response.url, parsed_url.path)

            if not absolute_url.startswith("http://") and not absolute_url.startswith("https://"):
                continue

            yield {
                "url": absolute_url,
                "original_url": link.url,
            }

            yield response.follow(link, self.parse)
