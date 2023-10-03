from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time

# Connect to BrightData via extension
extension_path = '.\extension.xpi'

options = Options()

def main():
    print('Connecting to Scraping Browser...')
    webdriver_service = Service('C:\Ron\Web Scraper\geckodriver-v0.33.0-win64\geckodriver.exe')
    driver = webdriver.Firefox(service=webdriver_service, options=options)
    driver.install_addon(extension_path, temporary=True)
    print('Connected! Navigating...')

    # Navigate to search
    driver.get('https://shopee.sg/search?keyword=razer%20blade')

    # Load page
    time.sleep(5)

    # Get product names and prices
    product_names = driver.find_elements(By.CSS_SELECTOR, '.Cve6sh')
    product_prices = driver.find_elements(By.CSS_SELECTOR, '.ZEgDH9')

    # Screenshot
    print('Taking page screenshot to file page.png')
    driver.get_screenshot_as_file('./page.png')

    # Print product names and prices
    for name, price in zip(product_names, product_prices):
        print(f'Product: {name.text}, Price: {price.text}')


if __name__ == '__main__':
    main()
