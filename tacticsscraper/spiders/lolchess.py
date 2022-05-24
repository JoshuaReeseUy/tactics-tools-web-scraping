import scrapy
import json
# Not Used, but main purpose is to scrape lolchess pages of top players to get more information on how many times each
# unit was used by each player. Tested it with Dishsoap2, the #1 player on the ladder at the time.
def clean(string):
    string = string.replace('\n', "")
    string = string.strip(" ")
    return string
class lolchessSpider(scrapy.Spider):
    name = "lolchess"
    start_urls = ['https://lolchess.gg/profile/na/dishsoap2']
    def parse(self, response):
            table = response.css('div.profile__recent__trends__units tr')
            for index, entry in enumerate(table):
                if index %  2 != 0:
                    yield {
                        'Champion': clean(entry.css('a::text').get()),
                        'Plays': clean(entry.css('td.plays::text').get())
                    }