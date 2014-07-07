# Scrapy settings for doubanmovie project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME         = 'doubanmovie'

SPIDER_MODULES   = ['doubanmovie.spiders']
NEWSPIDER_MODULE = 'doubanmovie.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'doubanmovie (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'doubanmovie.pipelines.MyImagesPipeline':1,
    'doubanmovie.pipelines.JsonWithEncodingPipeline': 300
}

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
IMAGES_STORE = 'posters-downloaded/'
LOG_LEVEL    = 'ERROR'