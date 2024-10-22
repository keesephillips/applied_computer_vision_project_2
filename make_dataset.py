import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time
import random

def scrape_images(query, num_images, save_path):
    print(f"\nDownloading {query}")
    
    imgs_saved = 0
    page = 1
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    driver = webdriver.Edge(r"C:\\Program Files\\msedgedriver.exe")
    driver.request_interceptor = lambda request: request.headers.update(headers)

    driver.maximize_window()
    
    query_formatted = query.replace(" ", "%20")
    search_url = f"https://pixabay.com/images/search/{query_formatted}/"

    driver.get(search_url)
    while imgs_saved < num_images:
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "link--WHWzm")))

        img_elements = driver.find_elements(By.TAG_NAME, "img")

        save_path = os.path.join(os.getcwd(), save_path)
        os.makedirs(save_path, exist_ok=True)

        for i, img_element in enumerate(img_elements):
            try:            
                src = img_element.get_attribute('src')
                if src != 'https://pixabay.com/static/img/blank.gif':
                    print('\rProgress:\t{:.2f}%'.format((imgs_saved / num_images) *100), end="")
                    img_data = requests.get(src).content
                    with open(f"{save_path}/{query}_{imgs_saved}.jpg", 'wb') as handler:
                        handler.write(img_data)
                        imgs_saved += 1
                if imgs_saved == num_images:
                    break

            except Exception as e:
                print(f"Failed to download image {i+1}: {e}")
        
        search_url = f"https://pixabay.com/images/search/{query}/?pagi={page}"
        driver.get(search_url)
        page += 1
        
    driver.quit()

query = "laptop"
num_images = 250
save_path = "laptop"
scrape_images(query, num_images, save_path)

query = "book"
num_images = 250
save_path = "book"
scrape_images(query, num_images, save_path)


