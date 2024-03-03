import time
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


def setup_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    print("Page opened")
    driver.implicitly_wait(10)
    return driver


def scroll_and_extract(driver, scroll_times=200, scroll_delay=1):
    for _ in range(scroll_times):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(scroll_delay)
    ytd_comments = driver.find_element(By.ID, 'comments')
    return ytd_comments.get_attribute('outerHTML')


def parse_and_format_comments(html):
    soup = BeautifulSoup(html, 'html.parser')
    comment_threads = soup.find_all('ytd-comment-thread-renderer')
    comments_data = [{
        'author': thread.find('a', {'id': 'author-text'}).text.strip() if thread.find('a', {
            'id': 'author-text'}) else 'Unknown',
        'comment': thread.find('yt-formatted-string', {'id': 'content-text'}).text.strip(),
        'likes': int(thread.find('span', {'id': 'vote-count-middle'}).text.strip()) if thread.find('span', {
            'id': 'vote-count-middle'}) and thread.find('span',
                                                        {'id': 'vote-count-middle'}).text.strip().isdigit() else 0,
        'age': thread.find('yt-formatted-string', {'class': 'published-time-text'}).text.strip() if thread.find(
            'yt-formatted-string', {'class': 'published-time-text'}) else 'Unknown'
    } for thread in comment_threads]
    return comments_data


def sanitize_title(title):
    return re.sub(r'\s+', '_', re.sub(r'[^\w\s-]', '', title))


def save_comments(comments_data, title):
    with open(f'{sanitize_title(title)}.json', 'w', encoding='utf-8') as json_file:
        json.dump(comments_data, json_file, ensure_ascii=False, indent=4)


def main(url):
    driver = setup_driver(url)
    title = driver.title
    print(title)
    time.sleep(10)
    comments_html = scroll_and_extract(driver)
    comments_data = parse_and_format_comments(comments_html)
    print(json.dumps(comments_data, ensure_ascii=False, indent=4))
    save_comments(comments_data, title)
    driver.quit()


if __name__ == "__main__":
    main("https://youtu.be/dKSrVSXvm4Y?si=vBPKrngUBoXyrIas")
