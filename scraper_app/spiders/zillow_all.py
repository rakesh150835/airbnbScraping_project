import scrapy
import json

class ZillowAllSpider(scrapy.Spider):
    name = "zillow_all"
    def __init__(self, city='', *args, **kwargs):
        super(ZillowAllSpider, self).__init__(*args, **kwargs)
        city1 = city.lower().replace(" ", "-").replace(",", "")
        self.city = city1
        self.url = f"https://www.zillow.com/{self.city}/rent-houses/"
        # file_name = city.replace(" ", "_").replace(",", "") + "-all.csv"
        # self.custom_settings = {
        #     'FEEDS': {
        #         file_name: {
        #             'format': 'csv',
        #             'overwrite': True,
        #         },
        #     },
        # }

    def start_requests(self):
        yield scrapy.Request(url=self.url,callback=self.parse)

    def parse(self, response):
        #//*[@id="grid-search-results"]/div[2]/nav/ul/li[6]/a
        next_data_script = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

        data = json.loads(next_data_script)

        homes = data['props']['pageProps']['searchPageState']['cat1']['searchResults']['listResults']

        for home in homes:
            #photos = [photo['url'] for photo in home.get('carouselPhotos',[])]
            photos = ','.join([f"'{photo['url']}'" for photo in home.get('carouselPhotos', [])])
            home_data = {
                "Property_address": home.get('address', None),
                "Listing_link": home.get('detailUrl', None),
                "Rent_price": home.get('price', None),
                "#bedrooms": home.get('beds', None),
                "#bathrooms": home.get('baths', None),
                "Square_footage": home.get('area', None),
                "images":f"[{photos}]"
            }
            yield home_data
        try:
            next_page_url = data['props']['pageProps']['searchPageState']['cat1']['searchList']['pagination'].get('nextUrl',None)
        finally:
            if (next_page_url):
                next_page_full_url = f'https://www.zillow.com' + data['props']['pageProps']['searchPageState']['cat1']['searchList']['pagination'].get('nextUrl',None)
                yield scrapy.Request(url=next_page_full_url,callback=self.parse)