from scrapy.spider import Spider
from scrapy.selector import Selector

from doubanmovie.items import MovieItem

class DoubanMovieSpider(Spider):
    name            = "doubanmovie"
    allowed_domains = ["douban.com"]
    start_urls = [
        "http://movie.douban.com/top250?start=%d" % d for d in range(0, 250, 25)
    ]

    def parse(self, response):
        sel   = Selector(response)
        sites = sel.css('.item')
        items = []
        for site in sites:
            item         = MovieItem()
            item['rank'] = site.xpath('div[@class="pic"]/em/text()').extract()[0]
            title_list   = site.css('.title::text').extract()
            for i in range(0,len(title_list)):
                title_list[i] = title_list[i].replace('/', '').strip()
            item['title'] = title_list[0]
            item['score']  = (float)(site.xpath('div[@class="info"]//div[@class="star"]//span/em/text()').extract()[0])
            quote = site.xpath('div[@class="info"]//p[@class="quote"]/span/text()').extract()
            if len(quote)>0:
                item['quote'] = quote[0]
            else:
                item['quote'] =''
            item['link']   = site.xpath('div[@class="info"]/div/a/@href').extract()[0]
            # http://img3.douban.com/view/photo/thumb/public/p1917567652.jpg
            # http://img3.douban.com/view/photo/photo/public/p1917567652.jpg
            # http://img3.douban.com/view/movie_poster_cover/ipst/public/p1917567652.jpg

            list = site.xpath('div[@class="pic"]/a/img/@src').extract()
            for i in range(0, len(list)):
                list[i] = list[i].replace('movie_poster_cover/ipst', 'photo/photo')
                if 'spic' in list[i]:  
                    list[i] = list[i].replace('spic','mpic')
            item['cover'] = list[0]
            items.append(item)
        return items
