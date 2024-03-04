import streamlit as st
import asyncio
import aiohttp
from typing import Tuple, Optional
from bs4 import BeautifulSoup
import json

# Constants
EXAM_RESULTS_URL = "https://exam.msrit.edu/"
UNSUCCESSFUL_LOOKUP_MESSAGE = "Oops!!! your USN could not be found in our result database, please verify the USN and click here to try again"

st.set_page_config(page_title="MSRIT Exam Results", page_icon=":bar_chart:", layout="centered")


def generate_payload(usn: str) -> dict:
    """Generate the payload for the POST request based on the USN."""
    return {
        "usn": usn.upper(),
        "osolCatchaTxt": "",
        "osolCatchaTxtInst": "0",
        "option": "com_examresult",
        "task": "getResult"
    }


def prepare_exam_lookup(usn: str) -> Tuple[str, dict]:
    """Prepare the URL and payload required for the exam result lookup."""
    return EXAM_RESULTS_URL, generate_payload(usn)


async def fetch_exam_results(url: str, payload: dict) -> Optional[str]:
    """Asynchronously post a request to the given URL with the payload and return the response text."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=payload) as response:
                response.raise_for_status()  # Raises an error for bad responses
                return await response.text()
        except aiohttp.ClientError as e:
            st.error(f"Request failed: {e}")
            return None


def is_result_available(soup: BeautifulSoup) -> bool:
    """Check if the result is available for the given USN."""
    center_tags = soup.find_all("center")
    if center_tags and center_tags[0].text.strip() == UNSUCCESSFUL_LOOKUP_MESSAGE:
        return False
    return True


def parse_exam_results(soup: BeautifulSoup) -> str:
    """Parse and return the exam results as a JSON string from the BeautifulSoup object."""
    if is_result_available(soup):
        result = {
            "name": soup.find("h3").text,
            "sgpa": soup.find_all("p")[3].text,
            "sem": soup.find("p").text.split(",")[-1].strip(),
            "image_src": soup.find_all("img")[1]['src']
        }
        return json.dumps(result, indent=4)
    else:
        err_msg = soup.find_all('center')[0].text.strip()
        results = {
            "error": f"{err_msg}"
        }
        return json.dumps(results, indent=4)


async def get_results(usn: str):
    url, payload = prepare_exam_lookup(usn)
    html_content = await fetch_exam_results(url, payload)
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
        return parse_exam_results(soup)
    return "Failed to retrieve results."


def main():
    st.title("MSRIT Exam Results")
    usn = ""
    usn = st.text_input("Enter your USN:", value=usn).upper()

    if st.button("Get Results"):
        if not usn:
            st.warning("Please enter a valid USN.")
            return

        with st.spinner("Fetching results..."):
            results = asyncio.run(get_results(usn))

        if results:
            if "error" in results:
                st.error(json.loads(results)["error"])
                return
            st.success("Results fetched successfully!")
            st.image(json.loads(results)["image_src"])
            st.write(f"Name: {json.loads(results)['name']}")
            st.write(f"Semester: {json.loads(results)['sem']}")
            st.write(f"SGPA: {json.loads(results)['sgpa']}")

        else:
            st.error("Failed to fetch results.")


if __name__ == "__main__":
    main()
