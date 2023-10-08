from selenium import webdriver
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from random import randint
from scrapycarou.class_names import class_names
import mysql.connector
import csv
import time

connection = mysql.connector.connect(
    user='jianrontan',
    password='Jianron101032%&g',
    host='localhost',
    database='carousell'
)
cursor = connection.cursor()

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

# Wait for page to load
wait = WebDriverWait(driver, 10)

# Check
print(f"{class_names[112]}")
print(f"{class_names[114]}")

# Scrape with beautifulsoup
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

elements_names = soup.find_all('p', class_='D_oy D_ov D_oz D_oC D_oG D_oJ D_oL D_oH D_oP')
product_names = [element.text for element in elements_names]

elements_prices = soup.find_all('p', class_='D_oy D_ov D_oz D_oC D_oF D_oJ D_oM D_oO')
product_prices = [element.text for element in elements_prices]

# Print product names and prices
for name, price in zip(product_names, product_prices):
    print(name, price)

# Store product names and prices in a .csv file
with open('products.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Price"])

    for name, price in zip(product_names, product_prices):
        writer.writerow([name, price])

# Store product names and prices in MySQL database
for name, price in zip(product_names, product_prices):
    add_product = ("INSERT INTO products "
                   "(name, price, date_time) "
                   "VALUES (%s, %s, NOW())")
    data_product = (name, price)
    cursor.execute(add_product, data_product)
    
connection.commit()
cursor.close()
connection.close()

time.sleep(10)
driver.quit()
time.sleep(1)