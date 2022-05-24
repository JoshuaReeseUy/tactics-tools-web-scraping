import scrapy
# Used for extracting data on the NA leaderboards on tactics.tools.
class LeaderboardSpider(scrapy.Spider):
    name = "players"
    start_urls = ['https://tactics.tools/leaderboards/na']
    def parse(self, response):
            players = response.css('div.lb-row')
            for i in range(0, len(players) // 2):
                yield{
                    'rank': players[2*i].css('div::text').getall()[0],
                    'name': players[2*i].css('div::text').getall()[2],
                    'patch-lp': players[2*i].css('div::text').getall()[3].strip('+'),
                    'lp': players[2*i].css('div::text').getall()[4].strip('LP'),
                    'patch-games': players[2*i].css('div::text').getall()[5],
                    'games': players[2*i].css('div::text').getall()[6],
                    'link': players[(2*i)+1].css('a::attr(href)').get()
                }
