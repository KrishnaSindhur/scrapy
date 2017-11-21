import scrapy

class Modest_mouse(scrapy.Spider):
    name = 'tree'
    start_urls = [
            'http://www.metrolyrics.com/modest-mouse-lyrics.html',
    ]
    def __init__(self):
        self.file = open('modest_mouse.txt', 'a')

    def parse(self, response):
        for href in response.css('.songs-table .title::attr(href)').extract():
            yield scrapy.Request(response.urljoin(href), callback = self.parse_song)

        next_page = response.css('.pagination .next::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_song(self, response):
        output = ''
        for stanza in response.css('#lyrics-body-text .verse::text'):
            output += stanza.extract().strip()
            output += '\n'
        self.file.write(output)
