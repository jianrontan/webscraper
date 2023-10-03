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

# Find and input query
search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search for anything and everything']")
search_box.send_keys('razer blade laptop')
time.sleep(randint(1,3))

# Click the search button
search_button = driver.find_element(By.XPATH, "//button[@type='submit']")
search_button.click()
time.sleep(randint(2,4))

# Scrape the data
product_elements = driver.find_elements(By.XPATH, "//p[@class='D_pw D_ov D_px D_pA D_pE D_pH D_pJ D_pF D_pN']")
product_names = [element.text for element in product_elements]

# Print out product names
for name in product_names:
    print(name)

time.sleep(10)
driver.quit()
time.sleep(1)