from selenium import webdriver
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from bs4.element import Tag
from random import randint
from scrapycarou.class_names import class_names
import mysql.connector
import csv
import time

def run(query):
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
    base_url = "https://www.carousell.sg"
    search_query = query
    query_words = search_query.lower().split()

    # Go to URL
    driver.get(url)
    time.sleep(randint(2,5))

    # Find and input query
    search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search for anything and everything']")
    search_box.send_keys(search_query)
    time.sleep(randint(1,3))

    # Click the search button
    search_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    search_button.click()
    time.sleep(randint(2,4))

    # Wait for page to load
    wait = WebDriverWait(driver, 10)

    # Check for marketplace
    try:
        marketplace_paragraph = driver.find_element(By.XPATH, "//p[@title='Marketplace']")
        marketplace_button = marketplace_paragraph.find_element(By.XPATH, "./..")
        marketplace_button.click()
        time.sleep(randint(3,5))
    except NoSuchElementException:
        pass

    # Get page source and write to a file
    page_source = driver.page_source
    with open('page_source.txt', 'w', encoding='utf-8') as f:
        f.write(page_source)

    # Scrape with beautifulsoup
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # Scrape anything in the page that has the search query words
    elements_names = [p for p in soup.find_all('p') if any(word in p.text.lower() for word in query_words)]
    product_names = [element.text for element in elements_names]

    # Scrape where the prices should be (if the price is missing, the 'product' won't be added to database)
    elements_prices = []
    for p in elements_names:
        try:
            price_div = p.find_next_sibling('div')
            if price_div:
                price_p = price_div.find('p')
                if price_p and 'S$' in price_p.text:
                    elements_prices.append(price_p)
                else:
                    elements_prices.append('')
                    print(f"Could not find price p tag for product {p.text}")
            else:
                elements_prices.append('')
                print(f"Could not find price div for product {p.text}")
        except AttributeError:
            elements_prices.append('')
            print(f"(AttributeError) Could not find price div for product {p.text}")
    product_prices = [element.text if isinstance(element, Tag) else element for element in elements_prices]

    # Scrape where the seller's username should be (if the username is missing, the 'product' won't be added to database)
    elements_sellers = []
    for p in elements_names:
        try:
            # Find the parent 'div' tag of the product name 'p' tag
            parent_div = p.find_parent('div')
            # Find the 'p' tag with data-testid="listing-card-text-seller-name" within the 'div' tag
            if parent_div:
                seller_p = parent_div.find('p', attrs={"data-testid": "listing-card-text-seller-name"})
                if seller_p:
                    elements_sellers.append(seller_p)
                else:
                    elements_sellers.append('')
                    print(f"Could not find seller p tag for product {p.text}")
            else:
                elements_sellers.append('')
                print(f"Could not find parent div for product {p.text}")
        except AttributeError:
            elements_sellers.append('')
            print(f"(AttributeError) Could not find parent div for product {p.text}")
    product_sellers = [element.text if isinstance(element, Tag) else element for element in elements_sellers]

    # Scrape where the links should be (if the link is missing, the 'product' won't be added to database)
    elements_links = []
    for p in elements_names:
        try:
            link_div = p.find_parent('a', href=True)
            if link_div and link_div['href'].startswith('/p/'):
                elements_links.append(base_url + link_div['href'])
            else:
                elements_links.append('')
                print(f"Could not find link div for product {p.text}")
        except AttributeError:
            elements_links.append('')   
            print(f"(AttributeError) Could not find link div for product {p.text}") 
    product_links = [base_url + element['href'] if isinstance(element, Tag) else element for element in elements_links]

    # Print product names, prices, and seller
    for name, price, seller in zip(product_names, product_prices, product_sellers):
        if price != '':
            print(name, price, seller)

    # Store product names, prices, sellers, and links in a .csv file
    with open('products.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Price", "Seller", "Link"])
        
        for name, price, seller, link in zip(product_names, product_prices, product_sellers, product_links):
            if price != '':
                writer.writerow([name, price, seller, link])
                
    # Create the table name
    table_name = search_query.replace(" ", "_")

    # Check if table exists, if not, create new table
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} "
                "(id INT AUTO_INCREMENT, name VARCHAR(255), price DECIMAL(10, 2), seller VARCHAR(255), link VARCHAR(1024), date_time DATETIME, PRIMARY KEY (id))")

    # Store product names and prices in MySQL database
    for name, price, seller, link in zip(product_names, product_prices, product_sellers, product_links):
        if price != '':
            price = price.replace('S$', '').replace(',', '')
            price = float(price)
            add_product = (f"INSERT INTO {table_name} "
                        "(name, price, seller, link, date_time) "
                        "VALUES (%s, %s, %s, %s, NOW())")
            data_product = (name, price, seller, link)
            cursor.execute(add_product, data_product)

    connection.commit()
    cursor.close()
    connection.close()

    time.sleep(10)
    driver.close()
    driver.quit()