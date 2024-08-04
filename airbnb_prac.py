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



def search_airbnb(location, checkin_date, checkout_date):
    # Open Airbnb
    driver.get("https://www.airbnb.com")

    # Wait for the page to load
    time.sleep(5)

    # Enter location
    location_input = driver.find_element(By.XPATH, "//input[@placeholder='Where are you going?']")
    location_input.clear()
    location_input.send_keys(location)

    # Wait for suggestions and select the first one
    time.sleep(2)
    location_input.send_keys(Keys.ARROW_DOWN)
    location_input.send_keys(Keys.RETURN)

    # Enter check-in date
    checkin_input = driver.find_element(By.XPATH, "//div[@data-testid='structured-search-input-field-datestart']")
    checkin_input.click()
    time.sleep(1)
    date_picker = driver.find_element(By.XPATH, f"//div[@data-testid='datepicker-day-{checkin_date}']")
    date_picker.click()

    # Enter check-out date
    checkout_input = driver.find_element(By.XPATH, "//div[@data-testid='structured-search-input-field-dateend']")
    checkout_input.click()
    time.sleep(1)
    date_picker = driver.find_element(By.XPATH, f"//div[@data-testid='datepicker-day-{checkout_date}']")
    date_picker.click()

    # Click the search button
    search_button = driver.find_element(By.XPATH, "//button[@data-testid='structured-search-input-search-button']")
    search_button.click()

    # Wait for results to load
    time.sleep(10)  # Adjust sleep time based on your internet speed

    # Get the current URL with search results
    search_results_url = driver.current_url
    print("Search Results URL:", search_results_url)

    # Close the browser
    driver.quit()

# Example usage
search_airbnb("New York", "2024-08-15", "2024-08-20")


driver.quit()