from fake_useragent import UserAgent
from scrapy import Spider, Request

class MySpider(Spider):
    name = 'spider'
    start_urls = ['https://www.carousell.sg/search/razer%20blade%20laptop?addRecent=true&canChangeKeyword=true&includeSuggestions=true&searchId=pJIBeQ']

    def start_requests(self):
        ua = UserAgent()
        for url in self.start_urls:
            yield Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0'})

    def parse(self, response):
        # Get all class names inside the <main> tag that start with "D_"
        class_names = response.css('main [class^="D_"] ::attr(class)').getall()

        # Store class names
        for class_name in class_names:
            print(class_name)
        
        # Store class names
        with open('class_names.py', 'w') as f:
            f.write(f"class_names = {class_names}")