# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class MovieItem(Item):
	rank        = Field()
	score       = Field()
	title       = Field()
	link        = Field()
	cover       = Field()
	quote       = Field()
	image_paths = Field()
