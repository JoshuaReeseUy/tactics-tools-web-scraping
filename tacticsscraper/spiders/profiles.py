import scrapy
import json

# Gets ratings made by tactics.tools on each players
class ProfileSpider(scrapy.Spider):
    name = "profiles"
    links = json.load(open('players.json'))
    start_urls = []
    for link in links:
        start_urls.append('https://tactics.tools' + link['link'])
    def parse(self, response):
            traits = response.css('text[font-family*="Merienda"]')
            name = response.css('div.notranslate::text').get()
            yield {
                     'Compositions': traits[0].css('text::text').get(),
                     'Econ': traits[1].css('text::text').get(),
                     'Flexibility': traits[2].css('text::text').get(),
                     'Execution': traits[3].css('text::text').get(),
                     'Items': traits[4].css('text::text').get(),
                     'name': name
                }