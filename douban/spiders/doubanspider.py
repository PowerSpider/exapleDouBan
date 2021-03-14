import scrapy
from scrapy_redis.spiders import RedisSpider


class DoubanspiderSpider(RedisSpider):
	name = 'doubanspider'
	allowed_domains = ['douban.com']
	start_urls = ['https://book.douban.com/tag/?view=cloud']
	
	def parse(self, response, **kwargs):
		for tag in response.css('.tagCol tr td a::attr(href)').getall():
			for page in range(49):
				yield scrapy.Request(url=f'https://book.douban.com{tag}?start={page * 20}&type=T',
					callback=self.parse_list)
	
	def parse_list(self, response):
		for uri in response.css('.subject-list .subject-item .info h2 a::attr(href)').getall():
			yield scrapy.Request(url=uri, callback=self.parse_detail)
	
	def parse_detail(self, response):
		item = {'title': response.css('h1 span ::text').get(), 'sorce': response.xpath('//strong/text()').get()}
		for detail in response.css('.indent #info'):
			item['author'] = detail.xpath('//span[@class="pl"][text()=" 作者"]/following-sibling::a/text()').get()
			item['publish_house'] = detail.xpath('//*[text()="出版社:"]/following-sibling::text()').get()
			item['Producer'] = detail.xpath('//*[text()="出品方:"]/following-sibling::a/text()').get()
			item['Producer_year'] = detail.xpath('//*[text()="出版年:"]/following-sibling::text()').get()
			item['page_num'] = detail.xpath('//*[text()="页数:"]/following-sibling::text()').get()
			item['price'] = detail.xpath('//*[text()="定价:"]/following-sibling::text()').get()
			item['Binding'] = detail.xpath('//*[text()="装帧:"]/following-sibling::text()').get()
			item['ISBN'] = detail.xpath('//*[text()="ISBN:"]/following-sibling::text()').get()
		print(item)
