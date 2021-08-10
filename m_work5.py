import time

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


client = MongoClient('127.0.0.1', 27017)
db = client['mail']
maildata = db['mail.ru']

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path='./chrdrv/chromedriver.exe', options=chrome_options)
driver.get('https://mail.ru/')

login = driver.find_element_by_xpath('//input[@name="login"]')
login.send_keys('study.ai_172@mail.ru'  .split('@')[0])
login.send_keys(Keys.ENTER)

time.sleep(1)

passwd = driver.find_element_by_xpath('//input[@type="password"]')
passwd.send_keys('NextPassword172!?')
passwd.send_keys(Keys.ENTER)

list_wait = WebDriverWait(driver, 15)
list_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'js-tooltip-direction_letter-bottom')))

mail_links = set()
makenext = True
mailcount = 0

links = driver.find_elements_by_class_name('js-tooltip-direction_letter-bottom')
driver.get(links[0].get_attribute('href'))
time.sleep(3)
body = driver.find_element_by_tag_name("body")
body.send_keys(Keys.CONTROL + Keys.ARROW_DOWN)

while makenext:
    link = driver.current_url
    # loading_wait = WebDriverWait(driver, 10)
    tag_from = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'letter-contact')))
    data = {
        'link': link,
        'folder': 'Входящие',
        'to': 'study.ai_172@mail.ru',
        'from': tag_from.get_attribute('title'),
        'fromlabel': tag_from.text,
        'title': driver.find_element_by_xpath('//h2[@class="thread__subject"]').text,
        'date': driver.find_element_by_xpath('//div[@class="letter__date"]').text,
        'content': driver.find_element_by_xpath('//div[@class="letter-body__body"]').text,
        }
    maildata.update_one(
                    {'link': data['link']},
                    {'$set': data},
                    upsert=True)

    time.sleep(3)
    try:
        body.send_keys(Keys.CONTROL + Keys.ARROW_DOWN)
    except:
        makenext = False




