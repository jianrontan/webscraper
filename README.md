# Web Scraper
This is a web app which activates an automated script that scrapes data off the popular e-commerce website Carousell.

## Features:
* Framework: [Flask](https://flask.palletsprojects.com/en/3.0.x/)
* Database: [MySQL](https://dev.mysql.com/doc/)
* Browser Automation: [Selenium](https://www.selenium.dev/documentation/)
* HTML Parsing: [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

## Overview:
This web scraper was built with the purpose of tracking the prices of products on Carousell over time.

### Description:
The user can enter a search query which will activate the script which will automatically navigate through the Carousell website to grab product titles, prices, sellers, links and the date and time. The user can also choose how many additional pages to scrape by adding a number to the "Number of extra pages" input field. The data collected will then be stored in the MySQL database. The user can then select a product to check and pick a range of prices to exclude (since people on Carousell like to set their price at $0), and a graph depicting the average price of the product over time will be displayed, as well as as table containing the last version of each product scraped. The user can click on a product, and a popup will appear, showing the price history and any other products (from the same search query) by the seller.

### Screenshots:

| Screenshots | Description |
|-|-|
| <img src="./screenshots/home.png" height="300" width="" alt="Home"> | Where the user can enter a search query to scrape, pick how many additional pages to scrape, select what search query data to display, and QC the results by picking the range of prices to exclude. |
| <img src="./screenshots/graph.png" height="300" width="960" alt="Graph"> | Graph of the average price of all results scraped against the date and time. |
| <img src="./screenshots/table.png" height="300" width="960" alt="Table"> | Table containing the data of last version of each product scraped. |
| <img src="./screenshots/popup.png" height="300" width="960" alt="Popup"> | After clicking on an individual product listing, this popup will appear, displaying the historical product data, as well as any other products from this search query by the same seller. |

### Design Choices:
<table>
  <tr>
    <td>Flask</td>
    <td>The decision to use flask was influenced by its integrated unit testing feature which allows for quick debugging, its simplicity and active community support.</td>
  </tr>
  <tr>
    <td>MySQL</td>
    <td>MySQL is a lightweight database management system that allows me to easily visualise all my data and serves the purposes of this project well.</td>
  </tr>
  <tr>
    <td>Selenium</td>
    <td>Selenium is a browser automation tool that allows me to select elements on the web page and interact with them</td>
  </tr>
  <tr>
    <td>Beautiful Soup</td>
    <td>Initially, I was able to obtain the page source but somehow, Selenium was unable to select the data I required from the page. Thus, Beautiful Soup was used and it proved to be more effective at parsing HTML</td>
  </tr>
</table>

### Explaining The Files:
| File | Description |
|-|-|
| script.py | This script is called for in the web app and accepts 2 arguments, the search query, and the number of extra pages. It connects to your MySQL database, opens the Carousell website on incognito, enters and submits the search query, loads the number of extra pages, and grabs the desired data and stores it in the database. It then closes the MySQL connection. |
| app.py |  |
| index.html |  |
| scripts.js |  |
| graph.js |  |
| styles.css |  |
