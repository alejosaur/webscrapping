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

        name = driver.find_element_by_class_name('product-name').text
        price = ""
        discount = ""
        discounted = ""

        try:
            price = driver.find_element_by_css_selector('[data-normal-price]').text.replace("$ ", "").split(' ')[0]
            discounted = driver.find_element_by_css_selector('[data-internet-price]').text.replace("$ ", "").split(' ')[0]
            discount = str(utils.calculate_discount(price, discounted)) + "%"
        except NoSuchElementException:
            price = driver.find_element_by_css_selector('[data-internet-price]').text.replace("$ ", "").split(' ')[0]
            discounted = driver.find_element_by_css_selector('[data-internet-price]').text.replace("$ ", "").split(' ')[0]
            discount = "0%"

        utils.save(url, name, price, discounted, discount)

        return {"product":name,
                "base_price":price,
                "discount":discount,
                "discounted_price":discounted}
    finally:
        driver.quit()