import scrapy
import json
from scrapy.crawler import CrawlerProcess
import time

class AirbnbSpider(scrapy.Spider):
    name = "airbnb"
    allowed_domains = ["airbnb.com"]
    start_urls = [
        'https://www.airbnb.co.in/s/New-York-City--New-York--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-09-01&monthly_length=3&monthly_end_date=2024-12-01&source=structured_search_input_header&search_type=unknown&price_filter_input_type=0&price_filter_num_nights=5&channel=EXPLORE&location_bb=QiOrmcKTZopCIejbwpSEpw%3D%3D&place_id=ChIJOwg_06VPwokRYv534QaPC8g&query=New%20York%20City%2C%20NY&date_picker_type=calendar'
    ]

    def parse(self, response):
        # Select the div with the class 'target-div'
        parent_div = response.xpath("//div[contains(@class, 'df8mizf atm_5sauks_glywfm dir dir-ltr')]")
        
        print("parent div: ", parent_div)
        
        divs = parent_div.css('div. dir dir-ltr')

        print("num of divs: ", len(divs))

        