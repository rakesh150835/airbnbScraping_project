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




driver.get('https://www.airbnb.com')

# Wait for a few seconds to allow the user to manually enter the location and dates
print("Please enter the location and dates in the browser.")
time.sleep(30)  # Adjust the time as necessary (in seconds)

# After the user has performed the search, retrieve the search result link
try:
    # Wait for the search results to load
    time.sleep(5)  # Adjust this as necessary based on your internet speed

    # Locate the first search result link (modify the selector based on the actual page structure)
    #result_link = driver.find_element(By.XPATH, '//a[contains(@class, "listing-link")]')  # Adjust the XPATH as needed

    #print("Search Result Link:", result_link.get_attribute('href'))

    print("Link: ", driver.current_url)

except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the browser
    driver.quit()