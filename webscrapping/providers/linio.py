from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from . import utils

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

def get(url):
    driver = webdriver.Chrome("./chromedriver")
    try:
        url = url.split("?")[0]
        driver.get(url)

        name = driver.find_element_by_class_name('product-name').text
        price = ""
        discount = ""
        discounted = ""

        try:
            price = driver.find_element_by_class_name('original-price').text.replace("$", "")
            discounted = driver.find_element_by_class_name('price-main-md').text.replace("$", "")
            discount = str(utils.calculate_discount(price, discounted)) + "%"
        except NoSuchElementException:
            price = driver.find_element_by_class_name('price-main-md').text.replace("$", "")
            discounted = driver.find_element_by_class_name('price-main-md').text.replace("$", "")
            discount = "0%"

        utils.save(url, "Linio", name, price, discounted, discount)

        return {"product":name,
                "base_price":price,
                "discount":discount,
                "discounted_price":discounted}
    finally:
        driver.quit()