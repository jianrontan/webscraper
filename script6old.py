from selenium import webdriver
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from random import randint
from scrapycarou.class_names import class_names
import pickle
import logging
import time

options = uc.ChromeOptions()
options.add_argument("--incognito")
driver = uc.Chrome(options=options)

url = "https://www.carousell.sg/"

# Go to URL
driver.get(url)
time.sleep(randint(2,5))

# Wait for page to load
wait = WebDriverWait(driver, 10)

# Find and input query
search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search for anything and everything']")
search_box.send_keys('razer blade laptop')
time.sleep(randint(1,3))

# Click the search button
search_button = driver.find_element(By.XPATH, "//button[@type='submit']")
search_button.click()
time.sleep(randint(2,4))

# Get page source and write to a file
page_source = driver.page_source
with open('page_source.txt', 'w', encoding='utf-8') as f:
    f.write(page_source)

# Scroll to mimic human behaviour
driver.execute_script("window.scrollTo(0, 720)")

# Scrape the data
product_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"//p[@class='D_oy D_ov D_oz D_oC D_oG D_oJ D_oL D_oH D_oP']")))
product_names = []
for element in product_elements:
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, element.get_attribute('xpath'))))
        product_names.append(element.text)
    except:
        continue

# Print out product names
for name in product_names:
    print(name)

time.sleep(20)
driver.quit()
time.sleep(1)