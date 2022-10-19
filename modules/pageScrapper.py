import time

from bs4 import BeautifulSoup
from modules.itemClass import Item
from selenium.webdriver.common.by import By

def getPageData(url, driver, writer):
    item_list = []
    driver.get(url)
    #print(driver.page_source)
    all_items = driver.find_elements(By.CLASS_NAME, 'list-row')
    for item in all_items:
        item_html = BeautifulSoup(item.get_attribute('outerHTML'), "html.parser")
        if item_html.find('span', {"class": "list-item-price"}):
            item = Item()
            item.sku = item_html.find('div', {"class":"advert-controls-save"}).get('data-id')
            item.name = item_html.find('div', {"class":"list-photo"}).findNext('a').findNext('img')['alt']
            item.image = item_html.find('div', {"class":"list-photo"}).findNext('a').findNext('img')['src']
            item.url = item_html.find('div', {"class":"list-photo"}).findNext('a')['href']
            item.price = item_html.find('span', {"class": "list-item-price"}).text.replace('€', '').strip()
            item.price_for_sqm = item_html.find('span', {"class": "price-pm"}).text.replace('€/m²', '').strip()
            item.num_of_rooms = item_html.find('td', {'class' : 'list-RoomNum'}).text.strip()
            item.overall_size = item_html.find('td', {'class' : 'list-AreaOverall'}).text.strip()
            item.floor = item_html.find('td', {'class' : 'list-Floors'}).text.replace('/', ' out of ').strip()

            item_list.append(item)

    for data in item_list:
        writer.writerow([data.sku, data.name, data.image, '=HYPERLINK("{}", "{}")'.format(data.url, data.url), data.price, data.price_for_sqm, data.num_of_rooms, data.overall_size, data.floor])
    
    print('{} items added'.format(len(item_list)))
            

    next_page_url = driver.find_elements(By.CSS_SELECTOR, ".pagination > a")

    if next_page_url[-1].get_attribute('class') != "page-bt-disabled":
        #print(next_page_url[-1].get_attribute('href'))
        time.sleep(3)
        getPageData(next_page_url[-1].get_attribute('href'), driver, writer)
    
    driver.quit()