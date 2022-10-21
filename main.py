import csv
import os

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from modules.pageScrapper import getPageData

from dotenv import load_dotenv

load_dotenv()

INITIAL_LINK = os.getenv("START_LINK")

currentTime = datetime.now()
ser = Service(os.path.abspath("assets/chromedriver.exe"))
options = Options()
options.add_argument("--window-size=640,480")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=ser, options=options)

csvfile = open(os.path.abspath('scrappedData/Data-'+currentTime.strftime("%m-%d-%Y_%H-%M")+'.csv'), 'w', encoding="Windows-1257", newline='')
writer = csv.writer(csvfile)
writer.writerow(['Sku', 'Name', 'Image', 'Url', 'Price', 'Price For Sqm', 'Number of rooms', 'Size', 'Floor'])
print("header written")

getPageData(INITIAL_LINK, driver, writer)

#print(item_list)
csvfile.close()


    
    
