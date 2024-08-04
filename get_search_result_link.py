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

# Navigate to Airbnb homepage
driver.get("https://www.airbnb.com")

# Wait for the page to fully load
time.sleep(5)



# Enter the location
location_input = driver.find_element(By.ID, 'bigsearch-query-detached-query-input')
location_input.send_keys("New York")  # Replace with your desired location
time.sleep(2)  # Wait for the location suggestions to load
location_input.send_keys(Keys.RETURN)

# Wait for location input to register
time.sleep(2)

# Open the check-in date picker and enter the check-in date
checkin_input = driver.find_element(By.XPATH, '//input[@id="checkin_input"]')
checkin_input.click()
time.sleep(1)
checkin_date = driver.find_element(By.XPATH, '//td[@data-testid="datepicker-day-2024-08-01"]')
checkin_date.click()

# Open the check-out date picker and enter the check-out date
checkout_input = driver.find_element(By.XPATH, '//input[@id="checkout_input"]')
checkout_input.click()
time.sleep(1)
checkout_date = driver.find_element(By.XPATH, '//td[@data-testid="datepicker-day-2024-08-05"]')
checkout_date.click()

# Click the search button
search_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
search_button.click()

# Wait for the results page to load
time.sleep(5)

# Get the current URL which is the search results URL
current_url = driver.current_url
print("Search results URL:", current_url)


# Close the browser
driver.quit()