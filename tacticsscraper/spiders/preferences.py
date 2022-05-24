import scrapy
import json

# Gets the most common units of every tactics.tools profile of the top 40 players on the NA leaderboard.
class UnitSpider(scrapy.Spider):
    name = "preferences"
    links = json.load(open('players.json'))
    start_urls = []
    for link in links:
        start_urls.append('https://tactics.tools' + link['link'])
    def parse(self, response):
            units = response.css('div.pr-2')[1:8]
            name = response.css('div.notranslate::text').get()
            dictionary = {'name': name}

            # for index, unit in enumerate(units):
            #     unit_name = (unit.css('::attr(src)').get())
            #     if len(unit_name.split('tft6_')) == 2:
            #         dictionary['unit' + str(index)] = unit_name.split('tft6_')[1].split('.jpg')[0].capitalize()
            #     else:
            #        dictionary['unit' + str(index)] = unit_name.split('tft6b_')[1].split('.jpg')[0].capitalize()

            yield dictionary