import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bS
import re

PATH = "/Applications/chromedriver"
download_dir = "/Users/h.vosskamp/Downloads/"


def scrape_page():
    driver = webdriver.Chrome(PATH)
    url = 'https://tenor.com/search/icon-gif-stickers'
    print(f"Scrape: {url}")
    driver.get(url)
    time.sleep(1)

    try:
        print("Page is ready!")

        elements = driver.find_elements(By.TAG_NAME, 'img')
        last_element = ''
        container_links = []
        while True:
            if len(elements) < 1 or last_element == elements[len(elements) - 1]:
                    break
            for element in elements:
                container_links.append(element.get_attribute("src"))
            last_element = elements[len(elements) - 1]
            driver.execute_script("arguments[0].scrollIntoView();", last_element)
            time.sleep(1)  # wait for page to load new content
            elements = driver.find_elements(By.TAG_NAME, 'img')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        container_links = list(set(container_links))
        for idx, link in enumerate(container_links):
            try:
                print(f"{idx} / {len(container_links)} Link: {link}")
                get_gif_and_write_to_disk(link)
            except Exception as e:
                print(link)
                print(e)
    except TimeoutException:
        print("Loading took too much time!")
    driver.quit()


def get_gif_and_write_to_disk(link):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    request = requests.get(link, headers=headers)
    last_slash = link.rfind('/')
    file_name = link[last_slash + 1:-4]
    with open(download_dir + file_name + '.gif', 'wb') as f:
        f.write(request.content)


if __name__ == '__main__':
    scrape_page()
    print("Done")
