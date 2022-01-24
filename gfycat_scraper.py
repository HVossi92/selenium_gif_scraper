import time

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

PATH = "/Applications/chromedriver"
download_dir = "/Users/h.vosskamp/Downloads/"

def scrape_page():
    driver = webdriver.Chrome(PATH)
    url = 'https://gfycat.com/stickers/search/icon+gifs'
    print(f"Scrape: {url}")
    driver.get(url)
    time.sleep(1)

    try:
        driver.execute_script("window.scrollBy(0,500)")
        print("Page is ready!")

        elements = driver.find_elements(By.CLASS_NAME, 'image')
        last_element = ''
        links = []
        while True:
            if last_element == elements[len(elements) - 1]:
                break
            for element in elements:
                links.append(element.get_attribute("src"))
            last_element = elements[len(elements) - 1]
            driver.execute_script("arguments[0].scrollIntoView();", last_element)
            time.sleep(1)  # wait for page to load new content
            elements = driver.find_elements(By.CLASS_NAME, 'image')

        links = list(set(links))
        for idx, link in enumerate(links):
            print(f"{idx} / {len(links)} Link: {link}")
            get_gif_and_write_to_disk(link)
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
