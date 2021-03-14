from scrapy.cmdline import execute


def alone():
	execute('scrapy crawl doubanspider'.split())


if __name__ == '__main__':
	alone()
