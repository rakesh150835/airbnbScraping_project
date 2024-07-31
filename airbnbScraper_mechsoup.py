import mechanicalsoup
from bs4 import BeautifulSoup
import time

# Create a browser object
browser = mechanicalsoup.StatefulBrowser()

# Open Airbnb website
browser.open("https://www.airbnb.com/rooms/556648170304299809?source_impression_id=p3_1720791935_P3jHQva76hGrccAp&check_in=2024-08-01&guests=1&adults=1&check_out=2024-08-05")

# title of the page
title = browser.page.select_one('title')
print("title: " + title.string)


# div tag for bedroom, bathroom
bath_bed_div_tag = browser.page.select_one('div.o1kjrihn atm_c8_km0zk7 atm_g3_18khvle atm_fr_1m9t47k atm_h3_1y44olf atm_c8_2x1prs__oggzyc atm_g3_1jbyh58__oggzyc atm_fr_11a07z3__oggzyc dir dir-ltr')

print("bath_bed_div_tag: " + str(bath_bed_div_tag))