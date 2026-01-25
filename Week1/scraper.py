from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

def fetch_url_content(url):
    try:
        response = requests.get(url=url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"[Error fetching {url}: {e}]"

    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""

    return (title + "\n\n" + text)[:2000]


def fetch_website_links(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    links = []
    for tag in soup.find_all("a"):
        href = tag.get("href")
        if href and not href.startswith(("#", "mailto:", "javascript:")):
            # Convert relative links to absolute
            full_url = urljoin(url, href)
            links.append(full_url)

    return links
