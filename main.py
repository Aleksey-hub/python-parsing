# 2) Написать программу, которая собирает «Новинки» с сайта техники mvideo и складывает данные в БД.
# Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары

import ast

from pymongo import MongoClient
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

chrome_options = Options()
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)

url = 'https://www.mvideo.ru/?cityId=CityCZ_2030'
driver.get(url)

# Закрываем окно с предложением авторизации
btn_wait = WebDriverWait(driver, 10)
try:
    btn_close = btn_wait.until(
        EC.presence_of_element_located((By.XPATH, '//span[@data-close="true"]')))
except TimeoutException:
    pass
else:
    btn_close.click()

# Пролистываем Новинки на сайте
actions = ActionChains(driver)
block_new_products = driver.find_element_by_xpath('//div[contains(h2, "Новинки")]')
actions.move_to_element(block_new_products).perform()  # без перемещения к блоку с новинками не работает
while True:
    try:
        btn_next = btn_wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[contains(h2, "Новинки")]/../..//a[contains(@class, "next-btn")]')))
    except TimeoutException:
        break
    except ElementClickInterceptedException:
        break
    else:
        btn_next.click()

# Собираем данные о Новинках
new_products = driver.find_elements_by_xpath(
    '//div[contains(h2, "Новинки")]/../..//a[contains(@class, "fl-product-tile-picture")]')

# Записываем в БД
client = MongoClient('127.0.0.1', 27017)
new_products_db = client['new_products_db']

for product in new_products:
    product_info = product.get_attribute('data-product-info')
    product_info_dict = ast.literal_eval(product_info)
    new_products_db.mvideo.insert_one(product_info_dict)
