import time
import json
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# scrape youtube comments
driver = webdriver.Chrome()
driver.get("https://youtu.be/dKSrVSXvm4Y?si=vBPKrngUBoXyrIas")
print("Page opened")
driver.implicitly_wait(10)
title = driver.title
print(title)
time.sleep(10)
for _ in range(20):
    driver.find_element(By.TAG_NAME, value="body").send_keys(u'\ue015')
time.sleep(10)

ytd_comments = driver.find_element(By.ID, value="comments")
comments_html = ytd_comments.get_attribute('outerHTML')
soup = BeautifulSoup(comments_html, 'html.parser')

total_comments = soup.find_all('yt-formatted-string')[0].text
print(total_comments)

comment_threads = soup.find_all('ytd-comment-thread-renderer')

comments_data = []
for thread in comment_threads:
    comment = thread.find('yt-formatted-string', {'id': 'content-text'}).text.strip()

    likes_tag = thread.find('span', {'id': 'vote-count-middle'}) or thread.find('span', {'id': 'vote-count-left'})
    likes = int(likes_tag.text.strip()) if likes_tag and likes_tag.text.strip().isdigit() else 0

    age_tag = thread.find('yt-formatted-string', {'class': 'published-time-text'})
    age = age_tag.text.strip() if age_tag else 'Unknown'

    author_tag = thread.find('a', {'id': 'author-text'})

    # Append to the list as a dictionary
    comments_data.append({
        'author': author_tag.text.strip() if author_tag else 'Unknown',
        'comment': comment,
        'likes': likes,
        'age': age
    })

# Convert the list to JSON format
comments_json = json.dumps(comments_data, ensure_ascii=False, indent=4)
print(comments_json)
# Write the JSON data to a file
title_sanitized = re.sub(r'[^\w\s-]', '', title)  # Remove unsupported characters
title_sanitized = re.sub(r'\s+', '_', title_sanitized)  # Replace spaces with underscores

# Write the JSON data to a file with the sanitized title
with open(f'{title_sanitized}.json', 'w', encoding='utf-8') as json_file:
    json.dump(comments_data, json_file, ensure_ascii=False, indent=4)

driver.quit()
