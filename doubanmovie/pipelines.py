# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import json
import codecs

from scrapy import signals
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
from PIL import Image


class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('json_data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):  
        image_guid = request.url.split('/')[-1]  
        return 'full/%s' % (image_guid)

    def get_media_requests(self, item, info):
        print item['rank']
        print item['cover']
        for image_url in item['cover']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
    	print item['rank']
        print item['cover']
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item