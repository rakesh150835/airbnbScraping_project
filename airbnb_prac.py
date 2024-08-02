import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Run headless if you do not need a browser window
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=service, options=options)


property_url = 'https://www.airbnb.co.in/rooms/28332501?adults=1&category_tag=Tag%3A8678&children=0&enable_m3_private_room=true&infants=0&pets=0&photo_id=1897962429&search_mode=regular_search&check_in=2024-08-02&check_out=2024-08-07&source_impression_id=p3_1722580760_P3gHrgL_6IWMT7xx&previous_page_section_name=1000&federated_search_id=12e269af-f2d6-4402-8c95-b1d3cb23ac03'
driver.get(property_url)

time.sleep(5)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# title of the page
print(soup.find('title').text)

# div tag for bedroom, bathroom
bath_bed_div_tag = soup.find('div', {'class':'o1kjrihn atm_c8_km0zk7 atm_g3_18khvle atm_fr_1m9t47k atm_h3_1y44olf atm_c8_2x1prs__oggzyc atm_g3_1jbyh58__oggzyc atm_fr_11a07z3__oggzyc dir dir-ltr'})

for list_tag in bath_bed_div_tag.ol.children:
    print(list_tag.text.strip())


# price tag
price_tag = soup.find_all('span', {'class':'_11jcbg2'})
print(price_tag[0].text)



# get all images
target_div = driver.find_element(By.XPATH, "//div[@class='_uhxsfg']")
parent_div = target_div.find_element(By.XPATH, "./parent::div")
parent_button = parent_div.find_element(By.XPATH, "./ancestor::button")

driver.execute_script("arguments[0].click();", parent_button)

time.sleep(10)


#--- different methods for image retrieval -----

imgsSrc = []
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

print(imgsSrc)
print(len(imgsSrc))




"""
def scroll_and_extract(driver, timeout=5):
    SCROLL_PAUSE_TIME = timeout
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    image_links = set()  # Use a set to avoid duplicates

    while True:
        # Scroll down slowly to load more images
        driver.execute_script("return window.scrollY")
        time.sleep(SCROLL_PAUSE_TIME)

        # Extract image links at the current scroll position
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        image_section = soup.find('div', {'class': '_cdo1mj'}) 
        if image_section:
            new_image_links = {img['src'] for img in image_section.find_all('img') if 'src' in img.attrs}
            image_links.update(new_image_links)

        # Scroll down 
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.PAGE_DOWN)
        #html.send_keys(Keys.PAGE_DOWN)
        #html.send_keys(Keys.PAGE_DOWN)
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    return list(image_links)

# Perform the scroll and extract
all_image_links = scroll_and_extract(driver)
for link in all_image_links:
    print(link)

#print(all_image_links)
print(len(all_image_links))

"""

driver.quit()