import scrapy
import json

class ZillowFurnishedSpider(scrapy.Spider):
    name = "zillow_furnished"
    def __init__(self, city='', *args, **kwargs):
        super(ZillowFurnishedSpider, self).__init__(*args, **kwargs)
        city1 = city.lower().replace(" ", "-").replace(",", "")
        self.city = city1
        self.current_page = 1
        self.base_url = f"https://www.zillow.com/{self.city}/rent-houses/"
        self.search_query_state = {
            "pagination": {"currentPage": self.current_page},
            "isMapVisible": True,
            "filterState": {
                "fr": {"value": True},
                "fsba": {"value": False},
                "fsbo": {"value": False},
                "nc": {"value": False},
                "cmsn": {"value": False},
                "auc": {"value": False},
                "fore": {"value": False},
                "tow": {"value": False},
                "mf": {"value": False},
                "con": {"value": False},
                "land": {"value": False},
                "apa": {"value": False},
                "manu": {"value": False},
                "apco": {"value": False},
                "att": {"value": "furnished"}
            },
            "isListVisible": True,
            "mapZoom": 13
        }
        self.url = self.base_url + '?searchQueryState=' + json.dumps(self.search_query_state)
        file_name = city.replace(" ", "_").replace(",", "") + "-furnished.csv"
        self.custom_settings = {
            'FEEDS': {
                file_name: {
                    'format': 'csv',
                    'overwrite': True,
                },
            },
        }
    def start_requests(self):
        yield scrapy.Request(url=self.url,callback=self.parse)

    def parse(self, response):
        #//*[@id="grid-search-results"]/div[2]/nav/ul/li[6]/a
        next_data_script = response.xpath('//script[@id="__NEXT_DATA__"]/text()').get()

        data = json.loads(next_data_script)

        homes = data['props']['pageProps']['searchPageState']['cat1']['searchResults']['listResults']

        for home in homes:
            photos = [photo['url'] for photo in home.get('carouselPhotos',[])]
            home_data = {
                "Property_address": home.get('address', None),
                "Listing_link": home.get('detailUrl', None),
                "Rent_price": home.get('price', None),
                "#bedrooms": home.get('beds', None),
                "#bathrooms": home.get('baths', None),
                "Square_footage": home.get('area', None),
                "images":photos
            }
            yield home_data
        try:
            next_page_url = data['props']['pageProps']['searchPageState']['cat1']['searchList']['pagination'].get('nextUrl', None)
            if next_page_url:
                self.current_page += 1
                self.search_query_state['pagination']['currentPage'] = self.current_page
                next_page_full_url = self.base_url +  '?searchQueryState=' + json.dumps(self.search_query_state)
                yield scrapy.Request(url=next_page_full_url, callback=self.parse)
        except:
            print("no more pages to scrape")