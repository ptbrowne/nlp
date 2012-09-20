# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class LyricsItem(Item):
    id = Field()
    title = Field()
    lyrics = Field()
    artists = Field()
    album = Field()
    genre = Field()
