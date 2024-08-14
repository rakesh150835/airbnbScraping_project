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
import gobnb


service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
#options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--lang=en-US")
#driver = webdriver.Chrome(service=service, options=options)

options.add_argument("--headless")
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
        self.image_links = []


    # function to get all listing properties on a particular page
    def get_property_listing(self, url):
        """
        This function takes the url of a particular page and get all the properties listing on that page. And it also get the pagination link of the next page.  
        """
        driver.get(url)

        time.sleep(5)
        page_source = driver.page_source
        soup_for_listings = BeautifulSoup(page_source, 'html.parser')

        property_listing = soup_for_listings.find_all('div', {'data-testid': 'card-container'})
        
        # get all the properties listed on a particular page
        listings = []
        for listing in property_listing:
            listings.append(listing.a['href'])

        time.sleep(3)
        # get the next page link from pagination
        try:
            pagination_tag = soup_for_listings.find('a', {'aria-label': 'Next'}).get('href')
            next_page_link = 'https://www.airbnb.com' + pagination_tag 
        except:
            next_page_link = None

        return next_page_link, listings
    

    def get_images_data(self, room_url, address):
        currency="USD"
        check_in = ""
        check_out = ""
        data = gobnb.Get_from_room_url(room_url,currency,check_in,check_out,"")
        images = data['images']

        image_links = []
        print(f"num of images for {address}: {len(images)}")
        for image in images:
            if image.get('url', None) != None:
                image_links.append(image.get('url'))

        return image_links

    # function to get property details
    def get_property_data(self, listings):
        """
            This function takes all the properties listed on a particular page and scrape the required data 
        """
        for listing in listings:
            property_url = 'https://www.airbnb.com' + listing
            
            driver.get(property_url)
            time.sleep(5)
            
            self.listing_link.append(property_url)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # address of the property
            address = ''
            try:
                address_tag = soup.find('div', {'class':'toieuka atm_c8_2x1prs atm_g3_1jbyh58 atm_fr_11a07z3 atm_cs_10d11i2 atm_c8_sz6sci__oggzyc atm_g3_17zsb9a__oggzyc atm_fr_kzfbxz__oggzyc dir dir-ltr'})
                address = address_tag.h2.text
                self.property_address.append(address)
            except:
                self.property_address.append('NA')


            # number of bedrooms, bathrooms
            try:
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
            except:
                self.bedrooms.append('1')
                self.bathroms.append('1')
                

            # price of the property
            try:
                price_tag = soup.find_all('span', {'class':'_11jcbg2'})
                price_text = price_tag[0].text
                if '\xa0' in price_text:
                    self.price.append(price_text.strip('\xa0'))
                else:
                    self.price.append(price_text)
            except:
                self.price.append('NA')


            # description of the property
            try:
                description_tag = soup.find('div', {'class':'d1isfkwk atm_vv_1jtmq4 atm_w4_1hnarqo dir dir-ltr'})
                description_text = description_tag.div.span.span.text
                self.listing_description.append(' '.join(description_text.split()))
            except:
                self.listing_description.append('NA')

            # get image links
            self.image_links.append(self.get_images_data(property_url, address))


    # get all data of all pages
    def get_all_data(self, url):
        """
            This function is used to get all data of every property.
            It uses the get_data function to get data of each property and
            hold the next page link url to get the properties listed on next page.
        """
        # this is line exceuted only once on main url 
        next_page_link, listings = self.get_property_listing(url)
        self.get_property_data(listings)

        try:
            while True:
                # get the next page link and property listings
                nextPageLink, listings = self.get_property_listing(next_page_link)
                next_page_link = nextPageLink
                self.get_property_data(listings)

                if not next_page_link:
                    break
        except:
            pass
        
        # dictionary to hold the scrapped data
        scraped_data = {
            'property_address': self.property_address, 'listing_link': self.listing_link, 'bedrooms': self.bedrooms, 
            'bathroms' : self.bathroms, 'square_footage': self.square_footage, 
            'price' : self.price, 'listing_description': self.listing_description, 'contact_name' : self.contact_name, 
            'contact_email' : self.contact_email, 
            'contact_phone_number' : self.contact_phone_number,
            'images': self.image_links 
            }

        # to add 'NA' value if data not found 
        max_length = 0
        for values in scraped_data.values():
            max_length = max(max_length, len(values))

        for key, values in scraped_data.items():
            if len(values) < max_length:
                values.extend(['NA']*(max_length - len(values)))

        # create dataframe to save data in csv file
        df = pd.DataFrame(scraped_data)
        df.to_csv('airbnb_data.csv', index=False)
        

#------- Driver Code -------

#city_name = 'flagstaff-az'
def scrape_airbnb(city_name):
    result_link = f'https://www.airbnb.com/s/{city_name}/homes?room_types%5B%5D=Entire%20home%2Fapt'

    if result_link:
        # new WebDriver instance to fetch the page source
        # options.add_argument("--headless")
        # driver = webdriver.Chrome(service=service, options=options)

        # object of the class
        scrap_object = Scrapper()
        # start scrapping
        scrap_object.get_all_data(result_link)

        driver.quit()