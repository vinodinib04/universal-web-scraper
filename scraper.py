import asyncio
import aiohttp
from bs4 import BeautifulSoup
from newspaper import Article
from urllib.parse import urljoin, urlparse
import markdownify
from config import MAX_DEPTH, MAX_PAGES

async def fetch_html(session, url):
    try:
        async with session.get(url, timeout=10) as resp:
            return await resp.text()
    except Exception:
        return ""

async def extract_links(session, base_url, html):
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        href = a['href']
        full_url = urljoin(base_url, href)
        if urlparse(full_url).netloc == urlparse(base_url).netloc:
            links.add(full_url)
    return list(links)

def extract_content(url, html):
    try:
        article = Article(url)
        article.download(input_html=html)
        article.parse()
        title = article.title
        content_md = markdownify.markdownify(article.text)
    except Exception:
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else "No Title"
        content_md = markdownify.markdownify(soup.get_text())

    return {
        "title": title.strip(),
        "content": content_md.strip(),
        "source_url": url
    }

def classify_content_type(content_text):
    text = content_text.lower()
    if "transcript" in text:
        return "podcast_transcript"
    elif "interview" in text:
        return "call_transcript"
    elif "linkedin.com" in text:
        return "linkedin_post"
    elif "reddit.com" in text:
        return "reddit_comment"
    elif len(text.split()) > 300:
        return "blog"
    else:
        return "other"

async def scrape_website(start_url):
    visited = set()
    to_visit = [(start_url, 0)]
    items = []

    async with aiohttp.ClientSession() as session:
        while to_visit and len(visited) < MAX_PAGES:
            url, depth = to_visit.pop(0)
            if url in visited or depth > MAX_DEPTH:
                continue

            html = await fetch_html(session, url)
            if not html:
                continue

            content_data = extract_content(url, html)
            content_data["content_type"] = classify_content_type(content_data["content"])

            items.append(content_data)
            visited.add(url)

            if depth < MAX_DEPTH:
                links = await extract_links(session, url, html)
                for link in links:
                    if link not in visited:
                        to_visit.append((link, depth + 1))

    return {
        "site": start_url,
        "items": items
    }
