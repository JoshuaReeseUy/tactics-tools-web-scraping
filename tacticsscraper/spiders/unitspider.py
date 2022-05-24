import scrapy
# Used for getting unit data (playrate, average placement, cost, etc.) on units from the units tab on tactics.tools.
class UnitSpider(scrapy.Spider):
    name = "units"
    start_urls = ['https://tactics.tools/units', 'https://tactics.tools/units/12.07']
    def parse(self, response):
            final_units_per_cost = ['Ziggs', 'Zyra', 'Zac', 'Vi']
            self.logger.info('hello this is my first spider')
            units = response.css('a[href*="/unit/"]')
            cost = 1
            patch = '12.7'
            for unit in units:
                yield {
                    'unit': unit.css('div::text').getall()[0],
                    'playrate': unit.css('div::text').getall()[1],
                    'placement': unit.css('div::text').getall()[2],
                    'patch': patch,
                    'cost': cost
                }
                last_unit = unit.css('div::text').getall()[0]
                if last_unit in final_units_per_cost:
                    cost += 1
