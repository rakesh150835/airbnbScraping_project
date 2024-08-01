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
options.add_argument("--headless")  # Run headless if you do not need a browser window
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=service, options=options)

property_address = []
listing_link = []
bedrooms = [] 
bathroms = [] 
square_footage = []
price = []
listing_description = [] 
contact_name = []
contact_email = [] 
contact_phone_number = []



# --- from here we will get listing ---
def get_preperty_listing(main_url):
    driver.get(main_url)

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
def get_property_data(listings):
    for listing in listings[:1]:
        property_url = 'https://www.airbnb.com' + listing
        driver.get(property_url)

        time.sleep(5)
        listing_link.append(property_url)
        #print('property url: ', property_url)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # title of the page
        address_tag = soup.find('div', {'class':'toieuka atm_c8_2x1prs atm_g3_1jbyh58 atm_fr_11a07z3 atm_cs_10d11i2 atm_c8_sz6sci__oggzyc atm_g3_17zsb9a__oggzyc atm_fr_kzfbxz__oggzyc dir dir-ltr'})
        address = address_tag.h2.text
        #print(address)
        property_address.append(address)


        # div tag for bedroom, bathroom
        bed = True
        bath = True
        for tag in soup.find_all('li', {'class':'l7n4lsf atm_9s_1o8liyq_keqd55 dir dir-ltr'}):
            text = tag.text.strip()
            if bed:
                for txt in text.split():
                    if txt in ['bed', 'bedroom', 'beds', 'bedrooms']:
                        for st in text.split():
                            if st.isdigit():
                                bedrooms.append(text[0])
                                bed = False
                                break
                        break
            if bed:
                bedrooms.append('1')
                bed = False
            
            if bath:
                for txt in text.split():
                    if txt in ['bath', 'bathroom', 'baths', 'bathrooms']:
                        for st in text.split():
                            if st.isdigit():
                                bathroms.append(text[0])
                                bath = False
                                break
                        break
            if bath:
                bathroms.append('1')
                bath = False

            #print(tag.text.strip())

        # price tag
        price_tag = soup.find_all('span', {'class':'_11jcbg2'})
        price_text = price_tag[0].text
        price.append(price_text)


        # description tag
        description_tag = soup.find('div', {'class':'d1isfkwk atm_vv_1jtmq4 atm_w4_1hnarqo dir dir-ltr'})
        description_text = description_tag.div.span.span.text
        #print(description_text)
        listing_description.append(description_text)






main_url = 'https://www.airbnb.com/s/Arizona--United-States/homes?flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-09-01&monthly_length=3&monthly_end_date=2024-12-01&query=Arizona%2C%20United%20States&place_id=ChIJaxhMy-sIK4cRcc3Bf7EnOUI&location_bb=QhQD0cLaFyFB%2BqikwuWh9Q%3D%3D&refinement_paths%5B%5D=%2Fhomes&tab_id=home_tab&date_picker_type=calendar&source=structured_search_input_header&search_type=autocomplete_click'

next_page_link, listings = get_preperty_listing(main_url)
get_property_data(listings)


try:
    while next_page_link:
        next_page_link, listings = get_preperty_listing(next_page_link)
        get_property_data(listings)
except:
    pass

# dictionary for scrapped data
scraped_data = {'property_address':property_address, 'listing_link':listing_link, 'bedrooms':bedrooms, 'bathroms':bathroms, 'square_footage':square_footage, 'price':price, 'listing_description':listing_description, 'contact_name':contact_name, 'contact_email': contact_email, 'contact_phone_number':contact_phone_number}

max_length = 0
for values in scraped_data.values():
    max_length = max(max_length, len(values))

for key, values in scraped_data.items():
    if len(values) < max_length:
        values.extend(['NA']*(max_length - len(values)))

df = pd.DataFrame(scraped_data)
df.to_csv('airbnb_US_1.csv', index=False)

print('------------')
#print(scraped_data)

print(next_page_link)



driver.quit()