import streamlit as st

from webscraper import get_html_content, soup_output, extract_text

st.title("Web Scraping")
st.subheader("Scraping websites with Python")

url = st.text_input("Enter a URL to scrape")
if url:
    html_content = get_html_content(url, use_selenium=False)
    soup = soup_output(html_content)
    if soup:
        title = soup.find("title")
        extracted_text = extract_text(soup)
        st.write(extracted_text)
