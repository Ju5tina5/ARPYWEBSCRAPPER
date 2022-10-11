import csv
from datetime import datetime
from re import I
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from modules.itemClass import Item
import os
import time


currentTime = datetime.now()
ser = Service(os.path.abspath("assets/chromedriver.exe"))
options = Options()
#options.headless = True
options.add_argument("--window-size=640,480")
driver = webdriver.Chrome(service=ser, options=options,)

item_list = []

def getPageData(url):
    driver.get(url)
    #print(driver.page_source)
    all_items = driver.find_elements(By.CLASS_NAME, 'list-row')
    for item in all_items:
        item_html = BeautifulSoup(item.get_attribute('outerHTML'), "html.parser")
        if item_html.find('span', {"class": "list-item-price"}):
            item = Item()
            item.name = item_html.find('div', {"class":"list-photo"}).findNext('a').findNext('img')['alt']
            item.image = item_html.find('div', {"class":"list-photo"}).findNext('a').findNext('img')['src']
            item.url = item_html.find('div', {"class":"list-photo"}).findNext('a')['href']
            item.price = item_html.find('span', {"class": "list-item-price"}).text.replace('€', '').strip()
            item.price_for_sqm = item_html.find('span', {"class": "price-pm"}).text.replace('€/m²', '').strip()
            item.num_of_rooms = item_html.find('td', {'class' : 'list-RoomNum'}).text.strip()
            item.overall_size = item_html.find('td', {'class' : 'list-AreaOverall'}).text.strip()
            item.floor = item_html.find('td', {'class' : 'list-Floors'}).text.replace('/', 'out of').strip()

            item_list.append(item)

            

    next_page_url = driver.find_elements(By.CSS_SELECTOR, ".pagination > a")

    if next_page_url[-1].get_attribute('class') != "page-bt-disabled":
        #print(next_page_url[-1].get_attribute('href'))
        time.sleep(3)
        getPageData(next_page_url[-1].get_attribute('href'))
    
    driver.quit()



getPageData("https://www.aruodas.lt/butai/vilniuje/?FRoomNumMin=1&FRoomNumMax=2&FHouseState=noteq&FOrder=Price")

#print(item_list)

with open('Data-'+currentTime.strftime("%m-%d-%Y_%H-%M")+'.csv', 'w', encoding="utf-16", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Image', 'Url', 'Price', 'Price For Sqm', 'Number of rooms', 'Size', 'Floor'])
    for data in item_list:
        writer.writerow([data.name, data.image, data.url, data.price, data.price_for_sqm, data.num_of_rooms, data.overall_size, data.floor])
