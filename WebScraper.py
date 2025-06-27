import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

# Base URL of the directory to crawl
BASE_URL = "https://cgi.cse.unsw.edu.au/~cs6453/24T2/"
DOWNLOAD_DIR = "cs6453_download"

# Set of visited URLs to prevent cycles
visited = set()


def is_valid_url(url):
    return url.startswith(BASE_URL)


def download_file(file_url, local_path):
    print(f"Downloading: {file_url}")
    response = requests.get(file_url)
    response.raise_for_status()
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as f:
        f.write(response.content)


def crawl_and_download(url, local_dir):
    if url in visited:
        return
    visited.add(url)

    print(f"Crawling: {url}")
    response = requests.get(url)
    response.raise_for_status()
    print(response.content)
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup.find_all("a"))
    for link in soup.find_all("a"):
        href: str = link.get("href")
        res = re.match(
            r"(?<=\/)[\-\w\.]+(?=\/)|(?<=\/)[\-\w\.]+|[\-\w.]+(?=\/)|^[\-\w\.]+", href
        )
        if (res) == None:
            continue

        full_url = urljoin(url, href)
        parsed = urlparse(full_url)
        relative_path = parsed.path.replace(urlparse(BASE_URL).path, "", 1).lstrip("/")
        local_path = os.path.join(local_dir, relative_path)

        if href.endswith("/"):
            crawl_and_download(full_url, local_dir)
        else:
            download_file(full_url, local_path)


# Start crawling and downloading
crawl_and_download(BASE_URL, DOWNLOAD_DIR)
print("✅ All files and subdirectories downloaded.")
