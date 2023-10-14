from selenium import webdriver
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pickle
import logging
import time

# Connect to BrightData
PROXY_HOST = ''
PROXY_PORT = ''
PROXY_USER = ''
PROXY_PASS = ''

def main():
    print('Connecting to Scraping Browser...')
    options = uc.ChromeOptions()
    # Connect to BrightData proxy
    options.add_argument(f'--proxy-server=https://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}')
    driver = uc.Chrome(options=options)
    print('Connected! Navigating...')

    # Navigate to Shopee
    driver.get('https://shopee.sg')
    driver.get_screenshot_as_file('./err_no_supported_proxies.png')

    # Load page
    time.sleep(10.369)

    # Close popup
    print('Taking page screenshot to file popup.png')
    driver.get_screenshot_as_file('./popup.png')
    actions = ActionChains(driver)
    actions.move_by_offset(369, 369).click().perform()
    print('Taking page screenshot to file popupclose.png')
    driver.get_screenshot_as_file('./popupclose.png')

    # Input query
    search_bar = driver.find_element(
        By.CLASS_NAME, 'shopee-searchbar-input__input')
    search_bar.send_keys('razer blade laptop')
    print('Taking page screenshot to file input.png')
    driver.get_screenshot_as_file('./input.png')

    # Wait a moment
    time.sleep(1.732)

    # Click the search button
    search_btn = driver.find_element(By.CLASS_NAME, 'shopee-searchbar__search-button')
    search_btn.click()

    # Screenshot
    print('Taking page screenshot to file page.png')
    driver.get_screenshot_as_file('./page.png')

    # Get product names and prices
    print('Navigated! Scraping page content...')
    product_names = driver.find_elements(By.CSS_SELECTOR, '.Cve6sh')
    product_prices = driver.find_elements(By.CSS_SELECTOR, '.ZEgDH9')

    # Screenshot
    print('Taking page screenshot to file page1.png')
    driver.get_screenshot_as_file('./page1.png')

    # Print product names and prices
    for name, price in zip(product_names, product_prices):
        print(f'Product: {name.text}, Price: {price.text}')


if __name__ == '__main__':
    main()
