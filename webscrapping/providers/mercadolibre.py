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

        url = url.split("?")[0]
        driver.get(url)

        name = driver.find_element_by_class_name('ui-pdp-title').text
        price = ""
        discount = ""
        discounted = ""

        try:
            discounted = driver.find_element_by_class_name('ui-pdp-price__second-line').find_element_by_class_name('price-tag-fraction').text
            price = driver.find_element_by_class_name('ui-pdp-price__original-value').find_element_by_class_name('price-tag-fraction').text
            discount = str(utils.calculate_discount(price, discounted)) + "%"
        except NoSuchElementException:
            price = driver.find_element_by_class_name('ui-pdp-price__second-line').find_element_by_class_name('price-tag-fraction').text
            discounted = driver.find_element_by_class_name('ui-pdp-price__second-line').find_element_by_class_name('price-tag-fraction').text
            discount = "0%"
            
        utils.save(url, "MercadoLibre", name, price, discounted, discount)

        return {"product":name,
                "base_price":price,
                "discount":discount,
                "discounted_price":discounted}
    finally:
        driver.quit()