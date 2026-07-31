import time
from collections import deque
from urllib.parse import urljoin, urlparse, urldefrag
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

START_URL = "https://atria.edu.in/"
ALLOWED_DOMAIN = "atria.edu.in"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/120 Safari/537.36"
    )
}

IGNORED_EXTENSIONS = (
    ".pdf", ".jpg", ".jpeg", ".png", ".gif", 
    ".svg", ".zip", ".docx", ".xlsx", ".mp4"
)

def clean_text(text):
    return " ".join(text.split())

def normalize_url(url):
    """Normalize URLs to prevent crawling the same page twice due to trailing slashes."""
    url, _ = urldefrag(url)
    parsed = urlparse(url)
    path = parsed.path.rstrip('/')
    return parsed._replace(path=path).geturl()

def is_valid_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in ["http", "https"]:
        return False

    if parsed.path.lower().endswith(IGNORED_EXTENSIONS):
        return False

    domain = parsed.netloc.lower()
    return domain == ALLOWED_DOMAIN or domain.endswith("." + ALLOWED_DOMAIN)

def extract_page(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()

        content_type = response.headers.get("Content-Type", "").lower()
        if "text/html" not in content_type:
            return None, []

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract links BEFORE decomposing navigation/footer elements
        links = []
        for link in soup.find_all("a", href=True):
            href = link.get("href")
            absolute_url = urljoin(url, href)
            normalized_url = normalize_url(absolute_url)

            if is_valid_url(normalized_url):
                links.append(normalized_url)

        # Decompose non-content structural elements
        for tag in soup(["script", "style", "noscript", "svg", "iframe", "form", "button", "nav", "footer"]):
            tag.decompose()

        title = ""
        if soup.title:
            title = clean_text(soup.title.get_text(" ", strip=True))

        main_content = soup.find("main") or soup.find("article") or soup.body
        if main_content is None:
            return None, []

        text = clean_text(main_content.get_text(" ", strip=True))

        page_data = {
            "url": url,
            "title": title,
            "text": text,
        }

        return page_data, links

    except requests.RequestException as error:
        print(f"\nCould not read {url}: {error}")
        return None, []

def crawl_website(start_url=START_URL, max_pages=80, delay=0.4):
    start_url = normalize_url(start_url)
    visited = set()
    queued = set([start_url])
    queue = deque([start_url])
    pages = []

    progress = tqdm(total=max_pages, desc="Crawling website")

    while queue and len(pages) < max_pages:
        current_url = queue.popleft()
        visited.add(current_url)

        page, links = extract_page(current_url)

        if page and len(page["text"]) >= 200:
            pages.append(page)
            progress.update(1)
            tqdm.write(f"Collected: {page['title'][:70]}")

        for link in links:
            if link not in visited and link not in queued:
                queued.add(link)
                queue.append(link)

        time.sleep(delay)

    progress.close()
    return pages

if __name__ == "__main__":
    crawled_data = crawl_website(max_pages=10)
    print(f"Total pages extracted: {len(crawled_data)}")