import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

HEADER = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.114 Safari/537.36",
    "Accept-Language": "en-us",
}
ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
             "%22mapBounds%22%3A%7B%22west%22%3A-122.74334944677734%2C%22east%22%3A-122.12330855322266%2C%22south%22" \
             "%3A37.65633635748451%2C%22north%22%3A37.89405545843448%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22" \
             "%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1" \
             "%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B" \
             "%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C" \
             "%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value" \
             "%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C" \
             "%22isListVisible%22%3Atrue%7D "
GOOGLE_FORM_URL = "google_form_url"  # Enter your Google Form url
CHROME_DRIVER_PATH = "chrome_driver_path"  # Enter your Chrome driver path
GOOGLE_EMAIL = "Gmail email address"  # Enter your Gmail email address
GOOGLE_PASSWORD = "Google account password"  # Enter your Google account password


class ZillowWebScraper:
    """A class used to scrape listing links, prices, and address from Zillow.com."""

    def __init__(self, zillow_url):
        self.zillow_url = zillow_url

    def scrape_listing_links(self) -> list:
        """
        Scrapes a provided Zillow URL for listing links using the Requests and BeautifulSoup4 packages.
        """
        response = requests.get(url=self.zillow_url, headers=HEADER)
        web_page = response.content

        soup = BeautifulSoup(markup=web_page, features="lxml")
        listing_link_anchors = soup.find_all(name="a", class_="list-card-link list-card-link-top-margin list-card-img")

        listing_links = []
        for element in listing_link_anchors:
            if "https://www.zillow.com" in element.get("href"):
                listing_links.append(element.get("href"))
            else:
                listing_links.append("https://www.zillow.com" + element.get("href"))

        print(listing_links)
        return listing_links

    def scrape_listing_prices(self) -> list:
        """
        Scrapes a provided Zillow URL for listing prices using the Requests and BeautifulSoup4 packages.
        """
        response = requests.get(url=self.zillow_url, headers=HEADER)
        web_page = response.content

        soup = BeautifulSoup(markup=web_page, features="lxml")
        listing_price_divs = soup.find_all(name="div", class_="list-card-price")

        listing_prices_raw = []
        for element in listing_price_divs:
            listing_prices_raw.append(element.get_text())

        stripped_prices_slashes = [price.split("/", 1)[0] for price in listing_prices_raw]
        stripped_prices_pluses = [price.split("+", 1)[0] for price in stripped_prices_slashes]
        listing_prices = [price.split(" ", 1)[0] for price in stripped_prices_pluses]

        print(listing_prices)
        return listing_prices

    def scrape_listing_addresses(self) -> list:
        """
        Scrapes a provided Zillow URL for listing addresses using the Requests and BeautifulSoup4 packages.
        """
        response = requests.get(url=self.zillow_url, headers=HEADER)
        web_page = response.content

        soup = BeautifulSoup(markup=web_page, features="lxml")
        address_tags = soup.find_all(name="address", class_="list-card-addr")

        listing_addresses = []
        for element in address_tags:
            listing_addresses.append(element.get_text())

        print(listing_addresses)
        return listing_addresses


class GoogleFormFiller:
    """A class used to fill and submit a Google Form with scraped listing data from Zillow.com."""

    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.listing_links = zws.scrape_listing_links()
        self.listing_prices = zws.scrape_listing_prices()
        self.listing_addresses = zws.scrape_listing_addresses()

    def fill_and_submit_forms(self):
        """
        Fills and submits a Google Form with scraped listing data from Zillow.com.
        """
        url = GOOGLE_FORM_URL

        for listing in range(len(self.listing_links)):
            self.driver.get(url)
            time.sleep(3)

            listing_address_input_box = self.driver.find_element_by_xpath(
                xpath='//*[@id="mG61Hd"]/div[2]/div/div[2]/div['
                      '1]/div/div/div[2]/div/div[1]/div/div[1]/input')
            listing_address_input_box.send_keys(self.listing_addresses[listing])

            time.sleep(3)

            listing_price_input_box = self.driver.find_element_by_xpath(
                xpath='//*[@id="mG61Hd"]/div[2]/div/div[2]/div['
                      '2]/div/div/div[2]/div/div[1]/div/div[1]/input')
            listing_price_input_box.send_keys(self.listing_prices[listing])

            time.sleep(3)

            listing_link_input_box = self.driver.find_element_by_xpath(
                xpath='//*[@id="mG61Hd"]/div[2]/div/div[2]/div['
                      '3]/div/div/div[2]/div/div[1]/div/div[1]/input')
            listing_link_input_box.send_keys(self.listing_links[listing])

            time.sleep(3)

            submit_form_button = self.driver.find_element_by_xpath(
                xpath='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span')
            submit_form_button.click()

    def create_sheet(self):
        """
        Creates a Google Sheet with Google Form data from fill_and_submit_forms().
        """
        url = "https://www.google.com/forms/about/"
        self.driver.get(url)

        time.sleep(3)

        go_to_google_forms_button = self.driver.find_element_by_class_name(name="mobile-device-is-hidden.js-dropdown"
                                                                                "-toggle")
        go_to_google_forms_button.click()

        google_sign_in_email_box = self.driver.find_element_by_xpath(xpath='//*[@id="identifierId"]')
        google_sign_in_email_box.send_keys(GOOGLE_EMAIL)

        time.sleep(3)

        google_sign_in_next_button = self.driver.find_element_by_xpath(xpath='//*[@id="identifierNext"]/div/button'
                                                                             '/div[2]')
        google_sign_in_next_button.click()


zws = ZillowWebScraper(zillow_url=ZILLOW_URL)
zws.scrape_listing_links()
zws.scrape_listing_prices()
zws.scrape_listing_addresses()

gff = GoogleFormFiller(driver_path=CHROME_DRIVER_PATH)
gff.fill_and_submit_forms()
gff.create_sheet()
