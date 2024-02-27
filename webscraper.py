import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

from url_list import website_urls


def extract_md(soup):
    converter = MarkdownConverter().convert_soup(soup)
    return converter


def get_html_content(url, use_selenium=False):
    if use_selenium:
        return fetch_html_with_selenium(url)
    else:
        return fetch_html_with_requests(url)


def fetch_html_with_selenium(url):
    options = uc.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--no-sandbox')
    driver = uc.Chrome(options=options, enable_cdp_events=True, version_main=114)

    try:
        driver.get(url)
        return driver.page_source
    finally:
        driver.quit()


def fetch_html_with_requests(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch URL: {url}")
        return None


def soup_output(html_content):
    if html_content:
        return BeautifulSoup(html_content, 'html.parser')
    else:
        return None


def extract_text(soup):
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text(separator="\n")
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text


def extract_urls(soup):
    urls = []
    for link in soup.find_all('a'):
        urls.append(link.get('href'))
    return urls


# Write the cleaned document to a text file
def write_to_file(content, filename):
    with open(f"txt_files/{filename}", 'w', encoding='utf-8') as file:
        file.write(content)


def create_md_file(content, filename):
    with open(f"md_files/{filename}", 'w', encoding='utf-8') as file:
        file.write(content)
        print(f"Created file: {filename}")


def run_in_loop():
    ino = 1
    for url in website_urls:

        html_content_ = get_html_content(url, use_selenium=True)
        soup = soup_output(html_content_)
        if soup:
            title = soup.find("title")
            print(title.text)
            txt_filename = f"webcontent{ino}.txt"
            md_filename = f"webcontent{ino}.md"
            ino += 1
            pretty_soup = soup.prettify()
            markdown_it = extract_md(pretty_soup)
            create_md_file(markdown_it, md_filename)
            # extracted_text = extract_text(soup)
            # print(extracted_text)
            # write_to_file(extracted_text, filename)
            # print(extract_urls(soup))
        else:
            print("Failed to parse HTML content.")


if __name__ == '__main__':
    # run_in_loop()
    url = "https://webtransparency.cs.princeton.edu/dark-patterns"
    itno = 1
    html_content = get_html_content(url, use_selenium=True)
    soup = soup_output(html_content)
    if soup:
        title = soup.find("title")
        txt_filename = f"webcontent{itno}.txt"
        md_filename = f"webcontent{itno}.md"
        pretty_soup = soup.prettify()
        markdown_it = extract_md(pretty_soup)
        create_md_file(markdown_it, md_filename)
        # extracted_text = extract_text(soup)
        # print(extracted_text)
        # write_to_file(extracted_text, txt_filename)
        # print(extract_urls(soup))
    else:
        print("Failed to parse HTML content.")
