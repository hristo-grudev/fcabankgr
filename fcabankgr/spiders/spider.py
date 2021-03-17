import scrapy

from scrapy.loader import ItemLoader

from ..items import FcabankgrItem
from itemloaders.processors import TakeFirst


class FcabankgrSpider(scrapy.Spider):
	name = 'fcabankgr'
	start_urls = ['https://www.fcabank.gr/who-we-are/news/']

	def parse(self, response):
		post_links = response.xpath('//article')
		for post in post_links:
			url = post.xpath('./a/@href').get()
			date = post.xpath('.//span[@class="news-date"]/text()').get()
			yield response.follow(url, self.parse_post, cb_kwargs={'date': date})

	def parse_post(self, response, date):
		title = response.xpath('//h1[@class="main-title__text-heading"]/text()').getall()
		title = [p.strip() for p in title]
		title = ' '.join(title).strip()
		description = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "main-title__text-desc", " " ))]//text()[normalize-space()] | //*[contains(concat( " ", @class, " " ), concat( " ", "main-body__quote__text--right", " " ))]//text()[normalize-space()] | //*[contains(concat( " ", @class, " " ), concat( " ", "main-body__text", " " ))]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=FcabankgrItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
