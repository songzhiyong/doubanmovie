# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
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
    index            = 0
    def __init__(self, basedir):
        self.index = 0
        super(MyImagesPipeline,self).__init__(basedir)

    def update_progress(self, progress):
        bar_length = 50
        end_val = 250
        percent = float(progress) / end_val
        hashes = '#' * int(round(percent * bar_length))
        spaces = ' ' * (bar_length - len(hashes))
        sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
        sys.stdout.flush()

    def file_path(self, request, response=None, info=None):  
        image_guid = request.url.split('/')[-1]  
        return 'full/%s' % (image_guid)

    def get_media_requests(self, item, info):
        for image_url in item['cover']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        self.update_progress(self.index)
        self.index = self.index + 1
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    