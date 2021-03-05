from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from . import utils

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

def get(url):
    try:
        driver = webdriver.Chrome("./chromedriver")

        driver.get(url)

        name = driver.find_element_by_class_name('product').text
        price = ""
        discount = ""
        discounted = ""

        try:
            price = driver.find_element_by_xpath('//span[@class="price-old"]').text.replace("$ ", "")
            discounted = driver.find_element_by_xpath('//span[@itemprop="price"]').text
            discount = str(utils.calculate_discount(price, discounted)) + "%"
        except NoSuchElementException:
            price = driver.find_element_by_xpath('//span[@itemprop="price"]').text
            discounted = driver.find_element_by_xpath('//span[@itemprop="price"]').text
            discount = "0%"

        return {"product":name,
                "base_price":price,
                "discount":discount,
                "discounted_price":discounted}
    finally:
        driver.quit()