# Scrapy settings for nlp project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'nlp'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['nlp.spiders']
NEWSPIDER_MODULE = 'nlp.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = [
'nlp.pipelines.MongoDBPipeline'
]
