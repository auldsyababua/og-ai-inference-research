#!/usr/bin/env python3
"""
Simple NVIDIA DCGM User Guide Scraper
======================================
Minimal dependency version - uses only standard library + requests/bs4
"""

import sys
import time
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse
from collections import OrderedDict

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("ERROR: Required packages not found.")
    print("Please install: pip3 install requests beautifulsoup4")
    sys.exit(1)


def fetch_page(url, session):
    """Fetch a page"""
    try:
        print(f"  Fetching: {url}")
        response = session.get(url, timeout=30)
        response.raise_for_status()
        time.sleep(0.5)
        return response.text
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def extract_links(soup, current_url):
    """Extract navigation links"""
    links = []

    # Find all links in navigation/sidebar
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.endswith('.html') and not href.startswith('#'):
            full_url = urljoin(current_url, href)
            if '/datacenter/dcgm/' in full_url and '/user-guide/' in full_url:
                links.append(full_url.split('#')[0])

    return list(OrderedDict.fromkeys(links))


def extract_title(soup):
    """Extract page title"""
    # Try h1 first
    h1 = soup.find('h1')
    if h1:
        return h1.get_text().strip()

    # Try title tag
    title = soup.find('title')
    if title:
        text = title.get_text().strip()
        # Clean up common suffixes
        text = re.sub(r'\s*[—\-|]\s*NVIDIA.*$', '', text)
        return text

    return "Untitled"


def html_to_markdown(soup):
    """Convert HTML to basic markdown"""
    # Remove unwanted elements
    for tag in soup.find_all(['script', 'style', 'nav', 'header', 'footer']):
        tag.decompose()

    # Find main content
    main = (soup.find('main') or
            soup.find('article') or
            soup.find('div', {'role': 'main'}) or
            soup.find('div', class_='document') or
            soup.find('div', class_='body') or
            soup.body or soup)

    # Remove navigation elements
    for elem in main.find_all(class_=['sphinxsidebar', 'related', 'footer']):
        elem.decompose()

    # Convert to markdown-ish format
    lines = []

    for elem in main.descendants:
        if elem.name == 'h1':
            lines.append(f"\n# {elem.get_text().strip()}\n")
        elif elem.name == 'h2':
            lines.append(f"\n## {elem.get_text().strip()}\n")
        elif elem.name == 'h3':
            lines.append(f"\n### {elem.get_text().strip()}\n")
        elif elem.name == 'h4':
            lines.append(f"\n#### {elem.get_text().strip()}\n")
        elif elem.name == 'p':
            text = elem.get_text().strip()
            if text:
                lines.append(f"\n{text}\n")
        elif elem.name == 'pre':
            code = elem.get_text().strip()
            if code:
                lines.append(f"\n```\n{code}\n```\n")
        elif elem.name == 'code' and elem.parent.name != 'pre':
            lines.append(f"`{elem.get_text().strip()}`")
        elif elem.name == 'li':
            text = elem.get_text().strip()
            if text and not any(child.name == 'ul' or child.name == 'ol' for child in elem.children):
                lines.append(f"- {text}\n")
        elif elem.name == 'a' and elem.get('href'):
            text = elem.get_text().strip()
            href = elem['href']
            if text and href:
                lines.append(f"[{text}]({href})")
        elif elem.name == 'img' and elem.get('src'):
            alt = elem.get('alt', 'Image')
            src = elem['src']
            lines.append(f"\n![{alt}]({src})\n")

    # Join and clean up
    markdown = ''.join(str(l) for l in lines)
    markdown = re.sub(r'\n\s*\n\s*\n+', '\n\n', markdown)
    return markdown.strip()


def scrape_dcgm_guide(base_url, output_path):
    """Main scraping function"""
    print("\n" + "="*70)
    print("NVIDIA DCGM User Guide Scraper")
    print("="*70)
    print(f"Starting URL: {base_url}")
    print(f"Output: {output_path}")
    print("="*70 + "\n")

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
    })

    visited = set()
    pages = OrderedDict()
    to_visit = [base_url]

    # Crawl pages
    print("Starting crawl...\n")
    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue

        print(f"[{len(visited)+1}] {url}")
        visited.add(url)

        html = fetch_page(url, session)
        if not html:
            continue

        soup = BeautifulSoup(html, 'html.parser')
        title = extract_title(soup)
        content = html_to_markdown(soup)

        pages[url] = {
            'title': title,
            'content': content
        }

        print(f"  ✓ {title}")

        # Find more pages
        links = extract_links(soup, url)
        new_links = [l for l in links if l not in visited]
        to_visit.extend(new_links)

        if new_links:
            print(f"  Found {len(new_links)} new pages")

    print(f"\n✓ Crawled {len(pages)} pages\n")

    # Generate markdown document
    print("Generating markdown document...")

    lines = []
    lines.append("# NVIDIA DCGM User Guide\n")
    lines.append(f"**Source:** {base_url}\n")
    lines.append(f"**Scraped:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n")
    lines.append("**Status:** Complete documentation from online source\n")
    lines.append("\n---\n")

    # Table of Contents
    lines.append("\n## Table of Contents\n")
    for i, (url, page) in enumerate(pages.items(), 1):
        title = page['title']
        anchor = re.sub(r'[^\w\s-]', '', title.lower()).replace(' ', '-')
        lines.append(f"{i}. [{title}](#{anchor})")
    lines.append("\n---\n")

    # Content
    for url, page in pages.items():
        lines.append(f"\n## {page['title']}\n")
        lines.append(f"*Source: {url}*\n")
        lines.append(page['content'])
        lines.append("\n---\n")

    # Footer
    lines.append(f"\n## Document Information\n")
    lines.append(f"- **Pages:** {len(pages)}")
    lines.append(f"- **Scraped:** {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    lines.append(f"- **Source:** {base_url}")
    lines.append("\n*This documentation is property of NVIDIA Corporation.*\n")

    markdown = '\n'.join(lines)

    # Save
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(markdown, encoding='utf-8')

    # Stats
    size_kb = len(markdown) / 1024
    print(f"\n✓ Saved successfully!")
    print(f"  File: {output_path}")
    print(f"  Size: {size_kb:.1f} KB")
    print(f"  Pages: {len(pages)}")
    print(f"  Characters: {len(markdown):,}\n")

    return 0


if __name__ == "__main__":
    base_url = "https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/index.html"
    output_path = "/srv/projects/og-ai-inference-research/docs/nvidia-manuals/NVIDIA-DCGM-User-Guide.md"

    try:
        sys.exit(scrape_dcgm_guide(base_url, output_path))
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
