from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import pickle

webdriver_service = Service('C:\Ron\Web Scraper\chromedriver-win64\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=webdriver_service)
driver.get("https://shopee.sg/login")

# Manually log in here
time.sleep(120)  # Wait for you to log in

# Save the cookies
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
driver.quit()
