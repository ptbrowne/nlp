from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from nlp.items import LyricsItem
from scrapy.http import Request
import re

def clean_html_but_br(string):
    return re.sub("<.*>", " ", string).split("\n \n")

class LetsSing(CrawlSpider):
    name = 'letsing'
    allowed_domains = ['letssingit.com']
    start_urls = ['http://artists.letssingit.com/artists/popular/3']

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(SgmlLinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(SgmlLinkExtractor(allow=('http://artists\.letssingit.com/.*/overview', ),
                               restrict_xpaths="//table[@class='data_list']"), 
             callback='parse_artist'),
    )

    def parse_artist(self, response):
        hxs = HtmlXPathSelector(response)

        top_list_song = hxs.select("//table[@id='toplist_songs']")
        for url in top_list_song.select(".//a/@href").extract()[2:4]:
            print url
            yield Request(url, callback=self.parse_lyrics)


    def parse_lyrics(self, response):
        hxs = HtmlXPathSelector(response)
        item = LyricsItem()
        item['id'] = response.url.split("-")[-1]
        item['title'] = "".join(hxs.select("//div[@class='center']//table//tr")[1].select(".//text()").extract()[1:])
        item['artists'] = hxs.select("//div[@class='center']//table//tr")[2].select(".//a//text()").extract()
        
        album = hxs.select("//div[@class='center']//table//tr")[3].select(".//text()").extract()[1:]
        if album:
            item['album'] = album[0]
        
        genre = hxs.select("//div[@class='center']//table//tr")[4].select(".//text()").extract()[1:]
        if genre:
            item['genre'] = genre[0].split(", ")
            
        item['lyrics'] = clean_html_but_br(hxs.select("//div[@id='lyrics']").extract()[0])
        return item 
