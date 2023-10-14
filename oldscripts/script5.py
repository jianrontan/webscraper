import time
from selenium import webdriver
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SBR_WEBDRIVER = 'https://'


def main():
    print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected! Navigating...')
        driver.get('https://www.carousell.sg/')
        print('Navigated! Scraping page content...')
        html = driver.page_source
        time.sleep(10.369)
        driver.get_screenshot_as_file('./screenshots/err_no_supported_proxies.png')
        search_bar = driver.find_element(
            By.CLASS_NAME, 'D_rU M_nb D_rV M_nc D_rH D_asT M_abg D_asN M_aaZ')
        search_bar.send_keys('razer blade laptop')
        print('Taking page screenshot to file input.png')
        driver.get_screenshot_as_file('./screenshots/input.png')

    # Wait a moment
        time.sleep(1.732)

    # Click the search button
        search_btn = driver.find_element(By.CLASS_NAME, 'D_pY M_lo D_qu D_qm M_lA D_qa M_lq D_qv D_asV M_abi D_asW M_abj') 
        search_btn.click() 

    # Screenshot
        print('Taking page screenshot to file page.png') 
        driver.get_screenshot_as_file('./screenshots/page.png') 

    # Get product names and prices
        print('Navigated! Scraping page content...') 
        product_names = driver.find_elements(By.CSS_SELECTOR, 'D_o_ D_ov D_oA D_oF D_oI D_oL D_oN D_oJ D_oR') 
        product_prices = driver.find_elements(By.CSS_SELECTOR, 'D_o_ D_ov D_oA D_oF D_oH D_oL D_oO D_oQ')

    # Screenshot
        print('Taking page screenshot to file page1.png')
        driver.get_screenshot_as_file('./screenshots/page1.png')

    # Print product names and prices
        for name, price in zip(product_names, product_prices):
            print(f'Product: {name.text}, Price: {price.text}')
            print(html)


if __name__ == '__main__':
    main()