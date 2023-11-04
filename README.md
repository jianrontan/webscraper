# Web Scraper
This is a web scraper to scrape data off carousell searches.

## Features:
* Framework: [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* Database: [MySQL](https://dev.mysql.com/doc/)
* Browser Automation: [Selenium](https://www.selenium.dev/documentation/)
* HTML Parsing: [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

## Overview:
This web scraper was built with the purpose of tracking the prices of products on carousell over time.

### Description:
The user can enter a search query which will activate the script which will automatically navigate through the carousell website to grab product titles, prices, sellers, links and the date and time. The user can also choose how many additional pages to scrape by adding a number to the "Number of extra pages" input field. The data collected will then be stored in the MySQL database. The user can then select a product to check and pick a range of prices to exclude (since people on carousell like to set their price at $0), and a graph depicting the average price of the product over time will be displayed, as well as as table containing the last version of each product scraped. The user can click on a product, and a popup will appear, showing the price history and any other products (from the same search query) by the seller.

### Screenshots:

| Screenshots | Description |
|-|-|
| <img src="./screenshots/home.png" height="400" width="600" alt="Home"> | Where the user can enter a search query to scrape, pick how many additional pages to scrape, select what search query data to display, and QC the results by picking the range of prices to exclude. |
| <img src="./screenshots/graph.png" height="400" width="600" alt="Graph"> | Graph of the average price of all results scraped against the date and time. |
| <img src="./screenshots/table.png" height="400" width="600" alt="Table"> | Table containing the data of last version of each product scraped. |
| <img src="./screenshots/popup.png" height="400" width="600" alt="Popup"> | After clicking on an individual product listing, this popup will appear, displaying the historical product data, as well as any other products from this search query by the same seller. |
