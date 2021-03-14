import requests
from typing import List
from loguru import logger
from parsel import Selector
from urllib.parse import quote


class DouBan:
	
	def __init__(self):
		self.tagURL = "https://book.douban.com/tag/?view=cloud"
		self.User_Agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
	
	def Scrape(self, URL):
		"""
		发送网络请求
		:param URL:
		:return:
		"""
		header = {
			"User-Agent": self.User_Agent
		}
		try:
			logger.debug(f'Scraping URL:{URL}')
			response = requests.get(url=URL, headers=header)
			if response.status_code == 200:
				return response.text
			logger.error(f"Send error when getting, URL:{URL}, status code{response.status_code}")
		except requests.RequestException:
			logger.error(f"RequestException when getting, URL:{URL}")
	
	def scrape_tag(self):
		"""
		获取tag page
		:return: Response
		"""
		return self.Scrape(self.tagURL)
	
	def parse_tag(self, tagResponse: str):
		"""
		解析tag页面
		:param tagResponse:
		:return: List
		"""
		selector = Selector(tagResponse)
		return selector.css('.tagCol tr td a::attr(href)').getall()
	
	def scrape_list(self, tags: List):
		"""
		获取 标签列表
		:param tags: List
		:example_ url https://book.douban.com/tag/%E6%B3%95%E5%9B%BD?start=980
		:return:
		"""
		for tag in tags:
			for page in range(49):
				tag_list_url = f'https://book.douban.com{quote(tag)}?start={page * 20}'
				yield self.Scrape(tag_list_url)
	
	def parse_list(self, list_page: str):
		"""
		解析其中的标签
		:param list_page:
		:return:
		"""
		selector = Selector(list_page)
		return selector.css('.subject-list .subject-item .info h2 a::attr(href)').getall()
	
	def scrape_detail(self, detail_href: list):
		"""
		:param detail_href:
		:return:
		"""
		# for uri in detail_href:
		return self.Scrape(detail_href)
	
	def parse_detail(self, detail_page):
		"""
		:param detail_page:
		:return:
		"""
		selector = Selector(detail_page)
		title = selector.css('h1 span ::text').get()
		sorce = selector.xpath('//strong/text()').get()
		for detail in selector.css('.indent #info'):
			author = detail.xpath('//span[@class="pl"][text()=" 作者"]/following-sibling::a/text()').get()
			publish_house = detail.xpath('//*[text()="出版社:"]/following-sibling::text()').get()
			Producer = detail.xpath('//*[text()="出品方:"]/following-sibling::a/text()').get()
			Producer_year = detail.xpath('//*[text()="出版年:"]/following-sibling::text()').get()
			page_num = detail.xpath('//*[text()="页数:"]/following-sibling::text()').get()
			price = detail.xpath('//*[text()="定价:"]/following-sibling::text()').get()
			Binding = detail.xpath('//*[text()="装帧:"]/following-sibling::text()').get()
			ISBN = detail.xpath('//*[text()="ISBN:"]/following-sibling::text()').get()


if __name__ == '__main__':
	# 初始化
	douban = DouBan()
	tagPage = douban.scrape_tag()
	tag_list = douban.parse_tag(tagPage)
	for list_page in douban.scrape_list(tag_list):
		for detail_href in douban.parse_list(list_page):
			detail_page = douban.scrape_detail(detail_href)
			douban.parse_detail(detail_page)
