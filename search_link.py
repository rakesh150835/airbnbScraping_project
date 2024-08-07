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
#options.add_argument("--headless")  # Run headless if not needed a browser window
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
#driver = webdriver.Chrome(service=service, options=options)




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


    # function to get all listing on a particular page
    def get_preperty_listing(self, url):
        driver.get(url)

        time.sleep(10)
        page_source = driver.page_source
        soup_for_listings = BeautifulSoup(page_source, 'html.parser')

        # property_listing_container = soup_for_listings.find('div', {'class': 'df8mizf atm_5sauks_glywfm dir dir-ltr'})
        property_listing = property_listing = soup_for_listings.find_all('div', {'data-testid': 'card-container'})

        
        listings = []
        for listing in property_listing:
            listings.append(listing.a['href'])

        pagination_tag = soup_for_listings.find('a', {'aria-label': 'Next'}).get('href')
        next_page_link = 'https://www.airbnb.com' + pagination_tag 

        return next_page_link, listings
    

    # function to get all images links of a particular property
    def get_images_links(self, driver):
        try:
            target_div = driver.find_element(By.XPATH, "//div[@class='_uhxsfg']")
            parent_div = target_div.find_element(By.XPATH, "./parent::div")
            parent_button = parent_div.find_element(By.XPATH, "./ancestor::button")

            driver.execute_script("arguments[0].click();", parent_button)

            time.sleep(5)

            driver.execute_script("window.scrollTo(0, 0);") #Go to top of page
            SCROLL_PAUSE_TIME = 5 #How long to wait between scrolls

            while True:
                previous_scrollY = driver.execute_script('return window.scrollY')
                
                html = driver.find_element(By.TAG_NAME, 'html')
                html.send_keys(Keys.PAGE_DOWN)
                html.send_keys(Keys.PAGE_DOWN) 
                time.sleep(SCROLL_PAUSE_TIME) 

                # Calculate new scroll height and compare with last scroll height
                #if previous_scrollY == driver.execute_script('return window.scrollY'):
                    #break
                

                images = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "itu7ddv atm_e2_idpfg4 atm_vy_idpfg4 atm_mk_stnw88 atm_e2_1osqo2v__1lzdix4 atm_vy_1osqo2v__1lzdix4 i1cqnm0r atm_jp_pyzg9w atm_jr_nyqth1 i1de1kle atm_vh_yfq0k3 dir dir-ltr")))
                # scroll to the last image, so that all images get rendered correctly
                driver.execute_script('arguments[0].scrollIntoView({block: "center", behavior: "smooth"});', images[-1])
                time.sleep(2)

                # PRINT URLS USING SELENIUM


                imgsSrc = []
                print("num of images: ", len(images))
                for img in images:
                    imgsSrc.append(img.get_attribute('src'))
                    print(img.get_attribute('src'))


                """
                containers = driver.find_elements(By.CLASS_NAME, "_cdo1mj")
                print("---containers---: ", len(containers))
                imgsSrc = []
                i = 0
                count = 0
                for container in containers:
                    if i == 5:
                        html = driver.find_element(By.TAG_NAME, 'html')
                        html.send_keys(Keys.PAGE_DOWN)
                        html.send_keys(Keys.PAGE_DOWN)
                        html.send_keys(Keys.PAGE_DOWN) 
                        time.sleep(SCROLL_PAUSE_TIME) 
                        i = 0
                    image = container.find_element(By.TAG_NAME, 'img')
                    print(image.get_attribute('src'))
                    imgsSrc.append(image.get_attribute('src'))
                    i += 1
                    count += 1
                
                if count == len(containers):
                    break
                """

            return imgsSrc
        except:
            return 'NA'

    def get_gobnb_data(self, room_url):
        currency="USD"
        check_in = ""
        check_out = ""
        data = gobnb.Get_from_room_url(room_url,currency,check_in,check_out,"")
        images = data['images']

        image_links = []
        for image in images:
            image_links.append(image['url'])

        return image_links


    # function to get property details
    def get_property_data(self, listings):
        for listing in listings[:1]:
            property_url = 'https://www.airbnb.com' + listing
            driver.get(property_url)

            time.sleep(5)
            
            self.image_links.append(self.get_gobnb_data(property_url))

            self.listing_link.append(property_url)
            print('property url: ', property_url)

            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # address of the property
            try:
                address_tag = soup.find('div', {'class':'toieuka atm_c8_2x1prs atm_g3_1jbyh58 atm_fr_11a07z3 atm_cs_10d11i2 atm_c8_sz6sci__oggzyc atm_g3_17zsb9a__oggzyc atm_fr_kzfbxz__oggzyc dir dir-ltr'})
                address = address_tag.h2.text
                #print(address)
                self.property_address.append(address)
            except:
                self.property_address.append('NA')


            # no. of bedrooms, bathrooms
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
                #print(tag.text.strip())

            # price tag
            try:
                price_tag = soup.find_all('span', {'class':'_11jcbg2'})
                price_text = price_tag[0].text[1:]
                if '\xa0' in price_text:
                    self.price.append(price_text[:-4])
                else:
                    self.price.append(price_text)
            except:
                self.price.append('NA')


            # description tag
            try:
                description_tag = soup.find('div', {'class':'d1isfkwk atm_vv_1jtmq4 atm_w4_1hnarqo dir dir-ltr'})
                description_text = description_tag.div.span.span.text
                #print(description_text)
                self.listing_description.append(' '.join(description_text.split()))
            except:
                self.listing_description.append('NA')

            # get image links
            #self.image_links.append(self.get_images_links(driver))


    # get all data of a particular location
    def get_all_data(self, url):
        next_page_link, listings = self.get_preperty_listing(url)
        self.get_property_data(listings)

        try:
            while True:
                nextPageLink, listings = self.get_preperty_listing(next_page_link)
                next_page_link = nextPageLink
                self.get_property_data(listings)
        except:
            print("error occured not going to next page")
        
        # dictionary for scrapped data
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

        # create dataframe to save in csv file
        df = pd.DataFrame(scraped_data)
        df.to_csv('airbnb_test_1.csv', index=False)

        print('------------')
        #print(scraped_data)

        #print(next_page_link)






# main url for the location 
#main_url = 'https://www.airbnb.com/s/Arizona--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2024-09-01&monthly_length=3&monthly_end_date=2024-12-01&price_filter_input_type=0&channel=EXPLORE&query=Arizona%2C%20United%20States&place_id=ChIJaxhMy-sIK4cRcc3Bf7EnOUI&location_bb=QhQD0cLaFyFB%2BqikwuWh9Q%3D%3D&date_picker_type=calendar&checkin=2024-08-10&checkout=2024-08-12&source=structured_search_input_header&search_type=autocomplete_click'

def get_search_result_link():
    # Set up the WebDriver (Make sure you have the correct WebDriver installed)
    driver = webdriver.Chrome(service=service, options=options)  # or webdriver.Firefox() for Firefox, etc.

    # Open the Airbnb website
    driver.get('https://www.airbnb.com')


    # Wait for a few seconds to allow the user to manually enter the location and dates
    print("Please enter the location and dates in the browser.")
    time.sleep(15)  # Adjust the time as necessary (in seconds)

    # After the user has performed the search, retrieve the search result link
    try:
        # Wait for the search results to load
        time.sleep(5)  # Adjust this as necessary based on your internet speed

        # Locate the first search result link (modify the selector based on the actual page structure)
        #result_link = driver.find_element(By.XPATH, '//a[contains(@class, "listing-link")]')  # Adjust the XPATH as needed

        #print("Search Result Link:", result_link.get_attribute('href'))

        main_url = driver.current_url

        print("---Main Link---: ", main_url)

    except Exception as e:
        print("An error occurred:", e)
        main_url = None

    finally:
            # Close the browser
            driver.quit()

    return main_url



# Main logic
#result_link = get_search_result_link()

city_name = 'new york'
result_link = f'https://www.airbnb.com/s/{city_name}/homes'


if result_link:
    # Open a new WebDriver instance to fetch the page source
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)

    scrap_object = Scrapper()

    # get to start scrapping
    scrap_object.get_all_data(result_link)

    driver.quit()
    
    print("Scrapping completed Successfully.")
else:
    print("No URL to fetch the page source.")


