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
options.add_argument("--headless")  # Run headless if you do not need a browser window
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=service, options=options)


property_url = 'https://www.airbnb.com/rooms/556648170304299809?source_impression_id=p3_1720791935_P3jHQva76hGrccAp&check_in=2024-08-01&guests=1&adults=1&check_out=2024-08-05'
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

# description tag
description_tag = soup.find('div', {'style':'line-height: 1.5rem; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 6; -webkit-box-orient: vertical;'})
description = description_tag.span.text
print(description)


print(soup.find('div', {'class': 'photo-viewer-section'}))

driver.quit()