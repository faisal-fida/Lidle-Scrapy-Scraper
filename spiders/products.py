import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import json


class ProductsSpider(scrapy.Spider):
    name = "products"

    le1 = LinkExtractor()
    allowed_domains = ["www.lidl.ie"]
    start_urls = ["https://www.lidl.ie/"]

    def start_requests(self):
        urls = json.load(open("links.json"))
        for u in urls:
            yield scrapy.Request(u["URL"])

    urls = []

    def parse(self, response):
        print("=" * 100)

        if "/p/" in response.url:
            title = response.xpath("//h1/text()").getall()
            title = "".join([t.strip() for t in title])
            price = response.xpath(
                '//article[@class="productbox"]//span[@class="pricebox__price"]/text()'
            ).get()
            if price:
                price = price.strip()

            id_1 = response.url.split("/")[-1]
            id_2 = response.xpath('//article[@class="productbox"]//img/@src').get()
            id_2 = re.findall("(article/)(.*)(/gallery)", id_2)[0][1]
            desc = response.xpath('//p[@itemprop="description"]/text()').get()
            if desc:
                desc = desc.strip()

            promo_date = response.xpath(
                '//article[@class="productbox"]//div[@class="ribbon__text"]/text()'
            ).get()
            base_price = ""
            if promo_date:
                promo = "Yes"
                base_price = response.xpath(
                    '//article[@class="productbox"]//div[@class="pricebox__highlight"]/text()'
                ).get()
                if base_price:
                    base_price = base_price.strip()
                promo_date = promo_date.strip()

            categories = response.xpath(
                '//div[@class="breadcrumbs__text"]/text()'
            ).getall()
            cats = categories[0] if len(categories) > 0 else ""
            subcats = categories[1] if len(categories) > 1 else ""
            yield {
                "URL": response.url,
                "Product ID1": id_1,
                "Product ID2": id_2,
                "Category": cats,
                "Sub Category": subcats,
                "Product Name": title,
                "Price": price,
                "Details": desc,
                "On Promo": "Yes" if promo_date else "No",
                "Original Price": base_price,
                "Promo Date": promo_date,
            }
