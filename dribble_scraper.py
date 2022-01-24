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
    url = 'https://dribbble.com/tags/icon_gifs'
    print(f"Scrape: {url}")
    driver.get(url)
    time.sleep(1)

    try:
        driver.execute_script("window.scrollBy(0,500)")
        print("Page is ready!")

        elements = driver.find_elements(By.CLASS_NAME, 'shot-thumbnail-link')
        last_element = ''
        container_links = []
        divider = ''
        while True:
            if len(elements) < 1 or last_element == elements[len(elements) - 1]:
                try:
                    new_divider = driver.find_element(By.CLASS_NAME, 'container-fluid')
                    if new_divider == divider:
                        break
                    divider = new_divider
                    driver.execute_script("arguments[0].scrollIntoView();", divider)
                    elements = driver.find_elements(By.CLASS_NAME, 'shot-thumbnail-link')
                except:
                    break
            for element in elements:
                container_links.append(element.get_attribute("href"))
            last_element = elements[len(elements) - 1]
            driver.execute_script("arguments[0].scrollIntoView();", last_element)
            time.sleep(4)  # wait for page to load new content
            elements = driver.find_elements(By.CLASS_NAME, 'shot-thumbnail-link')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
        }
        container_links = list(set(container_links))
        for idx, link in enumerate(container_links):
            request = requests.get(link, headers=headers).text
            category_soup = bS(request, 'lxml')
            try:
                gif_link = category_soup.find("img", src=re.compile("gif")).get("src")
                print(f"{idx} / {len(container_links)} Link: {gif_link}")
                get_gif_and_write_to_disk(gif_link)
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
