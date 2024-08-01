import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run headless if not needed a browser window
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=service, options=options)




class Scrapper():
    def __init__(self):
        self.property_address = []
        self.listing_link = []
        self.bedrooms = [] 
        self.bathroms = [] 
        self.square_footage = []
        self.price = []
        self.listing_description = [] 
        self.contact_name = []
        self.contact_email = [] 
        self.contact_phone_number = []


    # function to get all listing on a particular page
    def get_preperty_listing(self, url):
        
        driver.get(url)

        time.sleep(5)

        page_source = driver.page_source
        soup_for_listings = BeautifulSoup(page_source, 'html.parser')

        property_listing = soup_for_listings.find_all('div', {'data-testid': 'card-container'})
        listings = []
        for listing in property_listing:
            listings.append(listing.a['href'])

        pagination_tag = soup_for_listings.find('a', {'aria-label': 'Next'}).get('href')
        next_page_link = 'https://www.airbnb.com' + pagination_tag 

        return next_page_link, listings
        


    # function to get property details
    def get_property_data(self, listings):
        for listing in listings[:1]:
            property_url = 'https://www.airbnb.com' + listing
            driver.get(property_url)

            time.sleep(5)
            self.listing_link.append(property_url)
            print('property url: ', property_url)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # address of the property
            address_tag = soup.find('div', {'class':'toieuka atm_c8_2x1prs atm_g3_1jbyh58 atm_fr_11a07z3 atm_cs_10d11i2 atm_c8_sz6sci__oggzyc atm_g3_17zsb9a__oggzyc atm_fr_kzfbxz__oggzyc dir dir-ltr'})
            address = address_tag.h2.text
            #print(address)
            self.property_address.append(address)


            # no. of bedrooms, bathrooms
            bed = True
            bath = True
            for tag in soup.find_all('li', {'class':'l7n4lsf atm_9s_1o8liyq_keqd55 dir dir-ltr'}):
                text = tag.text.strip()
                if bed:
                    for txt in text.split():
                        if txt in ['bed', 'bedroom', 'beds', 'bedrooms']:
                            for st in text.split():
                                if st.isdigit():
                                    self.bedrooms.append(text[0])
                                    bed = False
                                    break
                            break
                if bed:
                    self.bedrooms.append('1')
                    bed = False
                
                if bath:
                    for txt in text.split():
                        if txt in ['bath', 'bathroom', 'baths', 'bathrooms']:
                            for st in text.split():
                                if st.isdigit():
                                    self.bathroms.append(text[0])
                                    bath = False
                                    break
                            break
                if bath:
                    self.bathroms.append('1')
                    bath = False

                #print(tag.text.strip())

            # price tag
            price_tag = soup.find_all('span', {'class':'_11jcbg2'})
            price_text = price_tag[0].text[1:]
            if '\xa0' in price_text:
                self.price.append(price_text[:-4])
            else:
                self.price.append(price_text)


            # description tag
            description_tag = soup.find('div', {'class':'d1isfkwk atm_vv_1jtmq4 atm_w4_1hnarqo dir dir-ltr'})
            description_text = description_tag.div.span.span.text
            #print(description_text)
            self.listing_description.append(description_text)



    def get_all_data(self, url):
        next_page_link, listings = self.get_preperty_listing(url)
        self.get_property_data(listings)


        try:
            while next_page_link:
                next_page_link, listings = self.get_preperty_listing(next_page_link)
                self.get_property_data(listings)
        except:
            pass

        # dictionary for scrapped data
        scraped_data = {}
        scraped_data['property_address'] = self.property_address, 
        scraped_data['listing_link'] = self.listing_link, 
        scraped_data['bedrooms'] = self.bedrooms, 
        scraped_data['bathroms'] = self.bathroms, 
        scraped_data['square_footage'] = self.square_footage, 
        scraped_data['price'] = self.price, 
        scraped_data['listing_description'] = self.listing_description, 
        scraped_data['contact_name'] = self.contact_name, 
        scraped_data['contact_email'] = self.contact_email, 
        scraped_data['contact_phone_number'] = self.contact_phone_number


        # to add 'NA' value if data not found 
        max_length = 0
        for values in scraped_data.values():
            max_length = max(max_length, len(values))

        for key, values in scraped_data.items():
            if len(values) < max_length:
                values.extend(['NA']*(max_length - len(values)))

        # create dataframe to save in csv file
        df = pd.DataFrame(scraped_data)
        df.to_csv('airbnb_US_4.csv', index=False)

        print('------------')
        print(scraped_data)

        print(next_page_link)




scrap_object = Scrapper()

# main url for the location 
main_url = 'https://www.airbnb.com/s/Arizona--United-States/homes?flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-09-01&monthly_length=3&monthly_end_date=2024-12-01&query=Arizona%2C%20United%20States&place_id=ChIJaxhMy-sIK4cRcc3Bf7EnOUI&location_bb=QhQD0cLaFyFB%2BqikwuWh9Q%3D%3D&refinement_paths%5B%5D=%2Fhomes&tab_id=home_tab&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click'
main_url = 'https://www.airbnb.com/s/Los-Angeles--California--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-09-01&monthly_length=3&monthly_end_date=2024-12-01&price_filter_input_type=0&channel=EXPLORE&query=Los%20Angeles%2C%20CA&place_id=ChIJE9on3F3HwoAR9AhGJW_fL-I&location_bb=QglZZ8LsT4JCBtCKwu1WGw%3D%3D&date_picker_type=calendar&checkin=2024-08-10&checkout=2024-08-12&source=structured_search_input_header&search_type=autocomplete_click'
# get to start scrapping
scrap_object.get_all_data(main_url)



driver.quit()